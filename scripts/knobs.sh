#!/usr/bin/env bash
# Reads the knob files of the tree under test and writes them as GitHub Actions outputs.
#
# A knob is on when its file exists under knobs/ AND this run changes it: the PR's own diff on pull_request, the
# group's diff (base_sha..head) on merge_group. So a knob file that merged into main is inert for later PRs; to use it
# again, change its content. Two exceptions look at the tree only: a root FAIL file, and the PAIR_A + PAIR_B pair.
set -euo pipefail

out="${GITHUB_OUTPUT:-/dev/stdout}"
event="${GITHUB_EVENT_NAME:-local}"

case "$event" in
  pull_request) changed="$(git diff --name-only HEAD^1 HEAD)" ;;          # checkout is the PR's merge commit
  merge_group) changed="$(git diff --name-only "$MERGE_GROUP_BASE" HEAD)" ;;
  *) changed="$(git diff --name-only HEAD^1 HEAD 2>/dev/null || true)" ;;
esac
echo "Changed in this run:"; sed 's/^/  /' <<<"$changed"

on() {  # on NAME: the knob file exists and this run changes it
  [ -e "knobs/$1" ] && grep -qx "knobs/$1" <<<"$changed"
}
word() {  # word NAME N: the Nth word of the knob file's first line
  head -n 1 "knobs/$1" | awk -v n="$2" '{print $n}'
}
scoped() {  # scoped NAME: on, and the event word in its content (if any) is this event
  on "$1" || return 1
  local v; v="$(head -n 1 "knobs/$1" | grep -oE 'pull_request|merge_group' | head -n 1 || true)"
  [ -z "$v" ] || [ "$v" = "$event" ]
}

fail=""; sleep_s=0; timeout=30; runner="ubuntu-latest"; skip=false; cancel=false; flaky=false
advisory=false; shards=false; status=""

[ -e FAIL ] && fail="root FAIL file present"
scoped FAIL && fail="knobs/FAIL"
if on FAIL_IN_QUEUE && [ "$event" = merge_group ]; then fail="knobs/FAIL_IN_QUEUE (merge_group only)"; fi
if [ -e knobs/PAIR_A ] && [ -e knobs/PAIR_B ] && { on PAIR_A || on PAIR_B; }; then
  fail="knobs/PAIR_A and knobs/PAIR_B are both in the tree (each is fine alone)"
fi
scoped FLAKY && flaky=true
if scoped SLOW; then sleep_s="$(word SLOW 1 | tr -cd '0-9')"; sleep_s="${sleep_s:-60}"; fi
if on HANG && [ "$event" = merge_group ]; then
  v="$(word HANG 1 | tr -cd '0-9')"; sleep_s="${v:-780}"            # 13 min: past the ruleset's 10-minute queue timeout
fi
if scoped TIMEOUT; then timeout=1; sleep_s=150; fi                 # the job runs past its own timeout-minutes
scoped NO_RUNNER && runner="tico-sandbox-no-such-runner"          # no runner has this label: queued until GitHub gives up (24 h)
scoped SKIP && skip=true
scoped CANCEL && cancel=true
on ADVISORY_RED && advisory=true
on SHARDS && shards=true
on STATUS && status="$(word STATUS 1)"

{
  echo "fail=$fail"; echo "sleep=$sleep_s"; echo "timeout=$timeout"; echo "runner=$runner"; echo "skip=$skip"
  echo "cancel=$cancel"; echo "flaky=$flaky"; echo "advisory=$advisory"; echo "shards=$shards"; echo "status=$status"
} | tee -a "$out"

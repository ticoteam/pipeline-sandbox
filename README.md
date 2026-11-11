# pipeline-sandbox

Test repo for Tico's Engineering pipeline: a real merge queue, one required check, and knobs that make GitHub fail in
the ways we have seen it fail. Nothing here ships.

- Ruleset "protect main": PR required (0 approvals), required check `checks` (GitHub Actions), merge queue (merge
  commits, ALLGREEN, build and merge up to 5, wait 1 minute, **10-minute check timeout**). Org admins may bypass on a
  PR only (`gh pr merge --admin`), as on ticoteam/tico. Nobody can push to main.
- Workflow `ci` runs on `pull_request` and `merge_group`: job `knobs` reads the knob files, then `checks` (required),
  `advisory` (not required) and, when asked, `shards` (not required). A plain run takes about 30 seconds.
- Workflow `release` (run by hand) tags `vN` and publishes a release. `shadow` runs only for knobs/SHADOW_RED.

## Knobs

Add or change a file under `knobs/` in the PR. A knob is on only when **this run changes that file**: the PR's own
diff on `pull_request`, the group's diff on `merge_group`. A knob file that merged into main is inert for later PRs; to
use it again, change its content (for example `echo 61 > knobs/SLOW` after a 60 merged). A PR queued
behind another one is built on top of it, so it inherits that PR's knobs in its `merge_group` run.

Where the content may name an event (`pull_request` or `merge_group`), the knob acts only on that event; no event means both.

| File | Content | What GitHub does |
|---|---|---|
| `FAIL` (repo root) | anything | `checks` red on both events (tree only: does not need to be in the diff) |
| `knobs/FAIL` | empty, or an event | `checks` red |
| `knobs/FAIL_IN_QUEUE` | anything | `checks` green on the PR, red in the merge queue: the PR is removed from the queue |
| `knobs/FLAKY` | empty, or an event | `checks` red on run attempt 1, green on any re-run (`gh run rerun <id> --failed`) |
| `knobs/SLOW` | seconds (default 60), then optionally an event: `120 merge_group` | `checks` sleeps that long |
| `knobs/HANG` | seconds (default 780) | `merge_group` only: `checks` sleeps 13 minutes then passes. The queue gives up at 10 minutes and removes the PR; the run then goes green anyway |
| `knobs/TIMEOUT` | empty, or an event | `checks` runs past its own 1-minute `timeout-minutes` |
| `knobs/CANCEL` | empty, or an event | the run cancels itself: `checks` ends `cancelled` |
| `knobs/NO_RUNNER` | empty, or an event | `checks` asks for a runner label nobody has: queued, never starts (GitHub drops it after 24 h). Cancel the run when done |
| `knobs/SKIP` | empty, or an event | `checks` is skipped by its `if:`. GitHub counts a skipped required check as passing |
| `knobs/NO_CHECK` | anything; the PR must change **only** this file | `ci` does not run on the PR (`paths-ignore`), so `checks` never reports: "Expected — waiting for status" |
| `knobs/ADVISORY_RED` | anything | `advisory` (not required) red; `checks` green. GitHub queues and merges it anyway |
| `knobs/SHARDS` | anything | `shards` (not required): shard 1 fails, fail-fast cancels shards 2 and 3 |
| `knobs/SHADOW_RED` | anything | workflow `shadow` adds a second check run named `checks`, red, on the PR head (not in the queue) |
| `knobs/STATUS` | `pending`, `success`, `failure` or `error` | a commit status `sandbox/status` (not a check run, not required) on the PR head. `pending` never resolves |
| `knobs/PAIR_A` + `knobs/PAIR_B` | anything | each alone is green. `checks` is red when both are in the tree and the run changes one: two PRs that pass alone fail when grouped in the queue, and the second stays red after the first merges |
| `conflict.txt` | one line | edit line 1 in two PRs: whichever merges second conflicts |

Two PRs that both add the same knob file with different content conflict with each other (add/add) once one merges;
queue them one at a time, or use different knobs. `knobs/HANG` keeps a PR in the queue for 10 minutes, which is the
easy way to act on a queued PR (close, dequeue, delete its branch).

GitHub refuses any push to the branch of a queued PR: "Branches that are queued for merging cannot be updated. To
modify this branch, dequeue the associated pull request." So a force-push after queueing needs a dequeue first.

Pushing twice quickly to a PR cancels the older `ci` run (`cancel-in-progress` on `pull_request`, like ticoteam/tico).

## Hand actions (not CI)

```bash
R=ticoteam/pipeline-sandbox
gh pr merge N -R $R                     # enqueue (the queue merges it); --admin merges past the queue
gh api graphql -f query='mutation{dequeuePullRequest(input:{id:"PR_NODE_ID"}){clientMutationId}}'   # dequeue by hand
gh run rerun RUN_ID -R $R --failed      # re-run (FLAKY passes)
git commit --amend --no-edit && git push -f   # force-push: a queued PR leaves the queue
gh pr ready N --undo / gh pr ready N    # draft and back
gh pr edit N --base OTHER_BRANCH        # retarget (stacked PRs)
gh pr close N / gh pr reopen N
git push origin --delete BRANCH         # delete the head branch under an open PR
```

## Release knobs

`gh workflow run release -R ticoteam/pipeline-sandbox -f mode=MODE [-f target=main~1] [-f slow_seconds=300]`

| mode | Result |
|---|---|
| `normal` | tag `v<N+1>` at `target` (default main), published release |
| `fail` | the run fails before tagging: no tag, no release |
| `tag-exists` | tries to publish the newest existing tag again: GitHub refuses, run red |
| `slow` | sleeps `slow_seconds`, then normal |
| `tag-only` | pushes the tag, then fails: a tag with no release (like v0.5.160 on Nov 5) |
| `draft` | a draft release: not published |
| `prerelease` | `v<N+1>-rc.1`, marked pre-release |
| `target=main~1` | any mode: a release that does not contain the newest merge |

Delete a release and its tag: `gh release delete vN -R ticoteam/pipeline-sandbox --cleanup-tag -y`.

The scenario catalogue that uses these knobs lives with Tico's pipelines-v3 reports (`sandbox-scenarios.md`).

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def negate(x):
    return -x


def multiply(a, b):
    for name, value in (("a", a), ("b", b)):
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"multiply() argument '{name}' must be a number, not {type(value).__name__}"
            )
    return a * b


def power(a, b):
    """Return a raised to b. Very large results may raise OverflowError or take a long time."""
    for name, value in (("a", a), ("b", b)):
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"power() argument '{name}' must be a number, not {type(value).__name__}"
            )
    if a == 0 and b < 0:
        raise ZeroDivisionError(
            "power() argument 'a' must not be zero when 'b' is negative"
        )
    if a < 0 and b % 1 != 0:
        raise ValueError("power() cannot raise a negative number to a non-whole power")
    return a**b


def modulo(a, b):
    """Return the remainder of a divided by b, with the sign of b: modulo(-7, 3) is 2."""
    for name, value in (("a", a), ("b", b)):
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"modulo() argument '{name}' must be a number, not {type(value).__name__}"
            )
    if b == 0:
        raise ZeroDivisionError("modulo() argument 'b' must not be zero")
    return a % b


def absolute_value(a):
    """Return a without its sign: absolute_value(-5) is 5."""
    if not isinstance(a, (int, float)):
        raise TypeError(
            f"absolute_value() argument 'a' must be a number, not {type(a).__name__}"
        )
    return abs(a)

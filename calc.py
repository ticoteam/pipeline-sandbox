import math


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


def sqrt(a):
    """Return the square root of a as a float: sqrt(9) is 3.0. A negative a raises ValueError."""
    if not isinstance(a, (int, float)):
        raise TypeError(
            f"sqrt() argument 'a' must be a number, not {type(a).__name__}"
        )
    if a < 0:
        raise ValueError("sqrt() argument 'a' must not be negative")
    return math.sqrt(a)


def cube_of(a):
    """Return a raised to the third power: cube_of(3) is 27."""
    if not isinstance(a, (int, float)):
        raise TypeError(
            f"cube_of() argument 'a' must be a number, not {type(a).__name__}"
        )
    return a**3


def floor_divide(a, b):
    """Return a divided by b, rounded down toward negative infinity: floor_divide(-7, 2) is -4."""
    for name, value in (("a", a), ("b", b)):
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"floor_divide() argument '{name}' must be a number, not {type(value).__name__}"
            )
    if b == 0:
        raise ZeroDivisionError("floor_divide() argument 'b' must not be zero")
    return a // b


def clamp(x, low, high):
    """Return x limited to the range low to high: clamp(15, 0, 10) is 10.

    The result is x, low or high unchanged, so its type can be int or float. low must not be greater than high.
    """
    for name, value in (("x", x), ("low", low), ("high", high)):
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"clamp() argument '{name}' must be a number, not {type(value).__name__}"
            )
    if low > high:
        raise ValueError("clamp() argument 'low' must not be greater than 'high'")
    if x < low:
        return low
    if x > high:
        return high
    return x


def sign(x):
    """Return -1, 0 or 1 for a negative, zero or positive x as an int: sign(-7) is -1.

    NaN compares false both ways, so sign(nan) is 0.
    """
    if not isinstance(x, (int, float)):
        raise TypeError(
            f"sign() argument 'x' must be a number, not {type(x).__name__}"
        )
    return (x > 0) - (x < 0)


def divide(a, b):
    for name, value in (("a", a), ("b", b)):
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"divide() argument '{name}' must be a number, not {type(value).__name__}"
            )
    if b == 0:
        raise ZeroDivisionError("divide() argument 'b' must not be zero")
    return a / b

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    for name, value in (("a", a), ("b", b)):
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"multiply() argument '{name}' must be a number, not {type(value).__name__}"
            )
    return a * b

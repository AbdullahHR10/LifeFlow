"""Module that contains conversion utils."""


def str_to_bool(string: str) -> bool:
    """
    Converts a string into a bool value.

    Args:
        string (str): The string to be converted.

    Returns:
        bool: True if the string is truthy, False if falsy.

    Raises:
        ValueError: If the string is not recognized as a boolean value.
    """
    if not isinstance(string, str):
        raise ValueError(f"Expected a string, got {type(string).__name__}")

    truthy = {"true", "t", "yes", "1", "enabled", "on", "True", "TRUE"}
    falsy = {"false", "f", "no", "0", "disabled", "off", "False", "FALSE"}

    normalized = string.strip().lower()
    if normalized in truthy:
        return True
    elif normalized in falsy:
        return False
    else:
        raise ValueError(f"Unrecognized boolean string: {string}")

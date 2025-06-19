"""Module that contains conversion utils."""
from datetime import datetime
from typing import Any, Tuple


def str_to_datetime(model: Any, fields: Tuple[str, ...] =
                    ("created_at", "updated_at")) -> None:
    """
    Converts the specified fields from ISO 8601 strings to datetime objects.

    Args:
        model (Any): The model instance to fix.
        fields (Tuple[str, ...]): Field names to
            check and convert if they are strings.

    Returns:
        None
    """
    for field in fields:
        value = getattr(model, field, None)
        if isinstance(value, str):
            setattr(model, field, datetime.fromisoformat(value))


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

    truthy = {"true", "t", "yes", "1", "enabled", "on"}
    falsy = {"false", "f", "no", "0", "disabled", "off"}

    normalized = string.strip().lower()
    if normalized in truthy:
        return True
    elif normalized in falsy:
        return False
    else:
        raise ValueError(f"Unrecognized boolean string: {string}")

"""Module that contains validators utils."""


def validate_string_field(
    key: str,
    value: str,
    min_length: int = 3,
    max_length: int = 30
) -> str:
    """
    Validates a short string field (e.g., name, title).

    Parameters:
        key (str): The name of the key being validated.
        value (str): The name to validate.
        min_length (int): Minimum allowed length.
        max_length (int): Maximum allowed length.

    Returns:
        str: The validated name value.

    Raises:
        ValueError: If the name is not between min_length
        and max_length characters.
    """
    if value is None or not isinstance(value, str):
        raise ValueError(f"{key} must be a non-empty string.")
    if len(value) > max_length or len(value) < min_length:
        raise ValueError(f"{key} must be between {min_length} and "
                         f"{max_length} characters.")

    return value

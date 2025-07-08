"""Module that contains validators utils."""
from marshmallow import ValidationError


def send_validation_error(field: str, message: str):
    """Raises a ValidationError that maps a field to a list of messages."""
    raise ValidationError({field: [message]})


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
        ValidationError: If the name is not between min_length
        and max_length characters.
    """
    if value is None or not isinstance(value, str) or len(value) == 0:
        send_validation_error(key, "must be a non-empty string.")
    if len(value) > max_length or len(value) < min_length:
        send_validation_error(key, f"must be between {min_length} and "
                              f"{max_length} characters.")

    return value


def validate_email(key: str, value: str) -> str:
    """
    Validates an email.

    Parameters:
        key (str): The name of the field being validated ('email').
        value (str): The email address to validate.

    Returns:
        str: The validated email address in lowercase and stripped.

    Raises:
        ValidationError: If the email format is invalid.
    """
    if value is None or not isinstance(value, str):
        send_validation_error(key, "must be a non-empty string.")

    value = value.strip().lower()

    if value.count('@') != 1:
        send_validation_error(key, "must contain exactly one '@' character.")

    if value.startswith('@') or value.endswith('@'):
        send_validation_error(key, "cannot start or end with '@'.")

    if value.startswith('.') or value.endswith('.'):
        send_validation_error(key, "cannot start or end with '.'.")

    if '..' in value:
        send_validation_error(key, "cannot contain consecutive dots ('..').")

    if '.' not in value.split('@')[1]:
        send_validation_error(key, "must contain a dot ('.') after the '@'.")

    return value

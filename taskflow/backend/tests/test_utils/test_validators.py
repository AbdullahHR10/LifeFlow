"""Module that contains validators tests."""
import pytest
from backend.utils.validators import validate_string_field, validate_email
from marshmallow import ValidationError


def test_valid_validate_string_field():
    """Tests validate_string_field with valid value."""
    value = "test"
    validate_string_field(None, value)


def test_invalid_validate_string_field():
    """Tests validate_string_field with invalid values."""
    values = ["aaa", "a" * 31]
    with pytest.raises(ValidationError, match="between 3 and 30 characters"):
        for value in values:
            validate_string_field(None, value)


def test_empty_string_validate_string_field():
    """Tests validate_string_field with an empty string."""
    values = [None, ""]
    with pytest.raises(ValidationError, match="non-empty string"):
        for value in values:
            validate_string_field(None, value)


def test_non_string_validate_string_field():
    """Tests validate_string_field with a non-string."""
    values = [1, 1.0, ["yes", 0], {"key": "value"}]
    with pytest.raises(ValidationError, match="non-empty string"):
        for value in values:
            validate_string_field(None, value)


def test_valid_validate_email():
    """Tests validate_string_field with valid email."""
    email = "test@example.com"
    validate_email(None, email)


def test_at_errors_validate_email():
    """Tests validate_email '@' errors emails."""
    emails = ["test", "test@@example.com"]
    with pytest.raises(ValidationError, match="exactly one '@' character"):
        for email in emails:
            validate_email(None, email)


def test_start_or_end_with_at_validate_email():
    """Tests validate_email with emails that start or end with '@'."""
    emails = ["@test", "test@"]
    with pytest.raises(ValidationError, match="start or end with '@'"):
        for email in emails:
            validate_email(None, email)


def test_start_or_end_with_dot_validate_email():
    """Tests validate_email with emails that start or end with '.'."""
    emails = [".test@", "test@."]
    with pytest.raises(ValidationError, match="start or end with '.'"):
        for email in emails:
            validate_email(None, email)


def test_consecutive_dots_validate_email():
    """Tests validate_email with a consecutive dots ('..') email."""
    email = "test@example..com"
    with pytest.raises(ValidationError, match="consecutive dots"):
        validate_email(None, email)


def test_no_dot_after_at_validate_email():
    """Tests validate_email with no '.' after '@' email."""
    email = "test@example"
    with pytest.raises(ValidationError, match="dot .* after the '@'"):
        validate_email(None, email)


def test_empty_string_validate_email():
    """Tests validate_email with an empty string."""
    values = [None, ""]
    with pytest.raises(ValidationError, match="non-empty string"):
        for value in values:
            validate_email(None, value)


def test_non_string_validate_email():
    """Tests validate_email with a non-string."""
    values = [1, 1.0, ["yes", 0], {"key": "value"}]
    with pytest.raises(ValidationError, match="non-empty string"):
        for value in values:
            validate_email(None, value)

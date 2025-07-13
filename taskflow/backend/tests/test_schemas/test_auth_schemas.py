"""Module that contains auth schema tests."""
import pytest
from backend.schemas.auth_schema import SignupSchema, LoginSchema
from marshmallow import ValidationError

signup_schema = SignupSchema()
login_schema = LoginSchema()


def test_valid_signup_schema():
    """Tests valid note schema."""
    data = {
        "name": "test",
        "email": "test@example.com",
        "password": "123456",
        "confirm_password": "123456"
    }
    loaded = signup_schema.load(data)

    assert loaded["name"] == "test"
    assert loaded["email"] == "test@example.com"
    assert loaded["password"] == "123456"
    assert loaded["confirm_password"] == "123456"


def test_invalid_signup_schema_missing_fields():
    """Tests signup schema with missing fields."""
    data = {}
    with pytest.raises(ValidationError) as e:
        signup_schema.load(data)
    assert "name" in e.value.messages
    assert "email" in e.value.messages
    assert "password" in e.value.messages
    assert "confirm_password" in e.value.messages


def test_invalid_signup_schema_short_password():
    """Tests signup schema with short password."""
    data = {
        "name": "test",
        "email": "test@example.com",
        "password": "123",
        "confirm_password": "123"
    }
    with pytest.raises(ValidationError) as e:
        signup_schema.load(data)
    assert "password" in e.value.messages


def test_invalid_signup_schema_password_mismatch():
    """Tests signup schema with mismatching passwords."""
    data = {
        "name": "test",
        "email": "test@example.com",
        "password": "123456",
        "confirm_password": "654321"
    }
    with pytest.raises(ValidationError) as e:
        signup_schema.load(data)
    assert "confirm_password" in e.value.messages
    assert "Passwords do not match." in e.value.messages["confirm_password"]


def test_valid_login_schema():
    """Tests valid login schema."""
    data = {
        "email": "test@example.com",
        "password": "123456"
    }
    loaded = login_schema.load(data)
    assert loaded["email"] == "test@example.com"
    assert loaded["password"] == "123456"
    assert loaded["remember"] is False


def test_invalid_login_schema_missing_fields():
    """Tests login schema with missing fields."""
    data = {}
    with pytest.raises(ValidationError) as e:
        login_schema.load(data)
    assert "email" in e.value.messages
    assert "password" in e.value.messages

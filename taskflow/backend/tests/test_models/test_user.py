"""Module that contains User class tests."""
import pytest
from backend import db
from backend.models import User
from sqlalchemy.exc import IntegrityError


def test_user_valid():
    """Tests valid email format."""
    user = User(name="test", email="test@example.com")
    user.password = "123456"

    assert isinstance(user.name, str)
    assert user.name == "test"
    assert isinstance(user.email, str)
    assert user.email == "test@example.com"
    assert isinstance(user._password, str)
    assert user.check_password("123456")


def test_name_cannot_be_none_or_empty():
    """Tests name cannot be None or empty."""
    with pytest.raises(ValueError, match="non-empty string"):
        User(name=None, email="test@example.com")


def test_name_cannot_be_non_string():
    """Tests name cannot be a non-string."""
    with pytest.raises(ValueError, match="non-empty string"):
        User(name=1, email="test@example.com")


def test_name_must_be_less_than_31_chars():
    """Tests name must be less than 31 characters."""
    with pytest.raises(ValueError, match="3 and 30 characters"):
        User(name="a" * 31, email="test@gmail.com")


def test_name_must_be_more_than_2_chars():
    """Tests name must be more than 2 characters."""
    with pytest.raises(ValueError, match="3 and 30 characters"):
        User(name="aa", email="test@gmail.com")


def test_email_cannot_be_none_or_empty():
    """Tests email cannot be None or empty."""
    with pytest.raises(ValueError, match="non-empty string"):
        User(name="test", email=None)


def test_email_cannot_be_non_string():
    """Tests email cannot be a non-string."""
    with pytest.raises(ValueError, match="non-empty string"):
        User(name="test", email=1)


def test_email_must_have_at_sign():
    """Tests email cannot be an invalid value."""
    with pytest.raises(ValueError, match="exactly one '@'"):
        User(name="test", email="")


def test_email_cannot_start_or_end_with_at():
    """Tests email cannot start or end with at."""
    with pytest.raises(ValueError, match="start or end with '@'"):
        User(name="test", email="@")


def test_email_cannot_start_with_dot():
    """Tests email cannot start or end with dot."""
    with pytest.raises(ValueError, match="start or end with '.'"):
        User(name="test", email=".@")


def test_email_cannot_end_with_dot():
    """Tests email cannot start or end with dot."""
    with pytest.raises(ValueError, match="start or end with '.'"):
        User(name="test", email="@.")


def test_email_cannot_contain_consecutive_dots():
    """Tests email cannot contain consecutive dot."""
    with pytest.raises(ValueError, match="consecutive dots"):
        User(name="test", email="a@..com")


def test_email_must_contain_a_dot():
    """Tests email must contain a dot after the at."""
    with pytest.raises(ValueError, match="contain a dot"):
        User(name="test", email="a@com")


def test_email_is_trimmed_and_lowercase():
    """Tests email is trimmed and lowercased."""
    user = User(name="test", email="   TEsT@EXaMPLe.COm   ")
    user.password = "123456"
    assert user.email == "test@example.com"


def test_email_is_unique(app, user):
    """Tests if user's email is unique."""
    user2 = User(name="user2", email="testemail@example.com")
    user2.password = "654321"

    with pytest.raises(IntegrityError):
        user2.save()


def test_users_can_have_same_name(app):
    user1 = User(name="duplicate", email="a@example.com")
    user1.password = "pwd1"
    user1.save()

    user2 = User(name="duplicate", email="b@example.com")
    user2.password = "pwd2"
    user2.save()


def test_password_write_only(user):
    """Tests that trying to access password will raise an error."""
    with pytest.raises(AttributeError, match="Password is write-only"):
        user.password


def test_password_cannot_be_none_or_empty_or_empty():
    """Tests password cannot be None or empty"""
    user = User(name="test", email="test@example.com")
    with pytest.raises(ValueError, match="non-empty string"):
        user.password = None
    with pytest.raises(ValueError, match="non-empty string"):
        user.password = ""
    with pytest.raises(ValueError, match="non-empty string"):
        user.password = 12345


def test_password_cannot_be_non_string():
    """Tests password cannot be a non-string."""
    with pytest.raises(ValueError, match="non-empty string"):
        user = User(name="test", email="test@example.com")
        user.password = 123456


def test_password_hashes_are_unique():
    """Tests 2 hashed password are unique"""
    user = User(name="test", email="test@example.com")
    user.password = "123456"
    hash1 = user._password

    user.password = "123456"
    hash2 = user._password

    assert hash1 != hash2


def test_check_password_with_wrong_password():
    """Tests check_password method with a wrong password."""
    user = User(name="test", email="test@example.com")
    user.password = "correct_password"
    assert not user.check_password("wrong_password")


def test_user_relationships_are_accessible():
    """Tests user relationships are present and accessible."""
    user = User(name="test", email="test@example.com")
    relations = ["tasks", "habits", "budgets", "transactions", "notes"]
    for relation in relations:
        assert hasattr(user, relation)
        assert isinstance(getattr(user, relation), list)


def test_user_to_dict_excludes_password():
    """Tests to_dict doesn't expose password."""
    user = User(name="test", email="test@example.com")
    user.password = "123456"
    d = user.to_dict()

    assert "password" not in d
    assert "_password" not in d


def test_str_method_excludes_password():
    """Tests __str__ doesn't expose password."""
    user = User(name="test", email="test@example.com")
    user.password = "123456"

    assert "password" not in str(user)

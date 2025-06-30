"""Module that contains BaseModel class tests."""
import pytest
from backend import db
from backend.models import User


def test_save_method(app):
    """Tests save presists and updates timestamp."""
    user = User(name="test", email="test@example.com")
    user.password = "123456"
    user.save()
    assert user.id is not None

    old_updated_at = user.updated_at
    user.name = "updated"
    user.save()
    assert user.updated_at > old_updated_at


def test_save_rollback_on_error(app, monkeypatch):
    """Tests save rolls back the database on error."""
    user = User(name="test", email="test@example.com")
    user.password = "123456"

    def fail_commit():
        raise Exception("DB commit failed")

    monkeypatch.setattr(db.session, "commit", fail_commit)

    with pytest.raises(Exception, match="DB commit failed"):
        user.save()


def test_delete_method(app):
    """Tests delete deletes instance."""
    user = User(name="test", email="test@example.com")
    user.password = "123456"
    user.save()
    user_id = user.id

    user.delete()
    assert db.session.query(User).filter_by(id=user_id).first() is None


def test_delete_rollback_on_error(app, monkeypatch):
    """Tests delete rolls back the database on error."""
    user = User(name="test", email="test@example.com")
    user.password = "123456"
    user.save()

    def fail_commit():
        raise Exception("DB commit failed")

    monkeypatch.setattr(db.session, "commit", fail_commit)

    with pytest.raises(Exception, match="DB commit failed"):
        user.delete()


def test_to_dict_method():
    """Tests to_dict returns a dict with object attributes."""
    user = User(name="test", email="test@example.com")
    user.password = "123456"
    d = user.to_dict()

    assert "id" in d
    assert "created_at" in d
    assert isinstance(d["created_at"], str)
    assert "updated_at" in d
    assert isinstance(d["updated_at"], str)
    assert d["name"] == "test"
    assert d["email"] == "test@example.com"

    assert "password" not in d


def test_str_method():
    """Tests __str__ returns a string representation of the object."""
    user = User(name="test", email="test@example.com")
    expected_str = f"[{user.__class__.__name__}] ({user.id}) {user.to_dict()}"
    assert expected_str == str(user)

"""Module that contains database helpers tests."""
import pytest
from backend.utils.db_helpers import (
    check_model, sanitize_input, get_object, build_object, edit_object)
from backend.models import BaseModel, User, Note
from backend.schemas.note_schema import NoteSchema
from werkzeug.exceptions import NotFound, HTTPException

note_schema = NoteSchema()


def test_valid_check_model():
    """Tests valid check_model."""
    check_model(Note)


def test_invalid_check_model():
    """Tests invalid check_model."""
    class FakeModel:
        pass

    with pytest.raises(NotFound) as exc_info:
        check_model(FakeModel)

    assert "model is unavailable" in str(exc_info.value.description)


def test_sanitize_input():
    """Tests sanitize_input."""
    data = {
        "title": "<script>alert('XSS')</script>",
        "content": "<b>Bold</b>",
        "safe": "Normal"
    }
    keys = ["title", "content", "safe"]
    cleaned = sanitize_input(data, keys)

    assert cleaned["title"] == "&lt;script&gt;alert('XSS')&lt;/script&gt;"
    assert cleaned["content"] == "<b>Bold</b>"
    assert cleaned["safe"] == "Normal"


def test_valid_get_object(logged_in_client, note):
    """Tests valid get_object."""
    obj = get_object(Note, note.id)

    assert obj.id == note.id
    assert obj.created_at == note.created_at
    assert obj.updated_at == note.updated_at
    assert obj.title == note.title
    assert obj.user_id == note.user_id


def test_none_user_id_get_object(client, note):
    """Tests none user_id get_object."""
    with pytest.raises(AttributeError, match="no attribute 'id'"):
        obj = get_object(Note, note.id)


def test_wrong_user_id_get_object(logged_in_client, note):
    """Tests wrong user_id get_object."""
    note.user_id = "123456"
    with pytest.raises(Exception, match="not found or unauthorized"):
        obj = get_object(Note, note.id)


def test_none_get_object(logged_in_client):
    """Tests wrong user_id get_object."""
    with pytest.raises(Exception, match="not found or unauthorized"):
        obj = get_object(Note, "123456")


def test_unavailable_model_get_object(logged_in_client):
    """Tests unavailable model get_object."""
    class Random(BaseModel):
        pass
    models = [BaseModel, User, Random]
    with pytest.raises(Exception, match="model is unavailable"):
        for model in models:
            obj = get_object(model, "123456")


def test_valid_build_object(logged_in_client):
    """Tests valid build_object."""
    note_data = {
        "title": "New Note",
        "content": "This is a test note.",
        "background_color": "BLUE"
    }
    keys = ["title", "content", "background_color"]
    new_note = build_object(Note, keys, note_schema, data=note_data)

    assert new_note.title == "New Note"
    assert new_note.content == "This is a test note."
    assert new_note.background_color == "BLUE"
    assert hasattr(new_note, "user_id")


def test_invalid_build_object(logged_in_client):
    """Tests invalid get_object."""
    note_data = {
        "content": "This is a test note.",
        "background_color": "BLUE",
        "hacker_field": "i'm a bad boy"
    }
    keys = ["title", "content", "background_color", "hacker_field"]

    with pytest.raises(HTTPException) as exc_info:
        build_object(Note, keys, note_schema, data=note_data)

    errors = ["Validation failed", "Unknown field", "Missing data"]

    assert exc_info.value.code == 400
    for error in errors:
        assert error in str(exc_info.value.description)


def test_valid_edit_object(logged_in_client, note):
    """Tests valid edit_object."""
    from copy import deepcopy
    old_note = deepcopy(note)

    note_data = {
        "title": "Edited Note",
        "content": "This is an edited note.",
        "background_color": "RED"
    }
    assert old_note.title != note_data["title"]

    keys = ["title", "content", "background_color"]
    edit_object(old_note, keys, note_schema, data=note_data)

    assert old_note.title == "Edited Note"
    assert old_note.content == "This is an edited note."
    assert old_note.background_color == "RED"


def test_invalid_edit_object(logged_in_client, note):
    """Tests invalid edit_object."""
    from copy import deepcopy
    old_note = deepcopy(note)

    note_data = {
        "content": "This is a test note.",
        "background_color": "BLUE",
        "hacker_field": "i'm a bad boy"
    }
    keys = ["content", "background_color", "hacker_field"]

    with pytest.raises(HTTPException) as exc_info:
        edit_object(old_note, keys, note_schema, data=note_data)

    assert exc_info.value.code == 400
    description = exc_info.value.description
    assert "hacker_field" in description["data"]
    assert "Unknown field." in description["data"]["hacker_field"]

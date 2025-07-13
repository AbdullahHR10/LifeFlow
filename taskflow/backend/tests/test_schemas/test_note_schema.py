"""Module that contains Note schema tests."""
import pytest
from backend.schemas.note_schema import NoteSchema
from marshmallow import ValidationError

note_schema = NoteSchema()


def test_valid_note_schema():
    """Tests valid note schema."""
    data = {
        "title": "test",
        "content": "test",
        "background_color": "BLUE"
    }
    loaded = note_schema.load(data)

    assert loaded["title"] == "test"
    assert loaded["content"] == "test"
    assert loaded["background_color"] == "BLUE"


def test_invalid_note_schema():
    """Tests invalid note schema."""
    data = {
        "background_color": "INVALID_COLOR"
    }
    with pytest.raises(ValidationError) as e:
        note_schema.load(data)
    assert "title" in e.value.messages
    assert "content" in e.value.messages
    assert "background_color" in e.value.messages


def test_note_schema_title_too_short():
    """Tests note schema title too short."""
    data = {
        "title": "aa",
    }
    with pytest.raises(ValidationError) as e:
        note_schema.load(data)
    assert "title" in e.value.messages


def test_note_schema_title_too_long():
    """Tests note title too long."""
    data = {
        "title": "a" * 31,
    }
    with pytest.raises(ValidationError) as e:
        note_schema.load(data)
    assert "title" in e.value.messages

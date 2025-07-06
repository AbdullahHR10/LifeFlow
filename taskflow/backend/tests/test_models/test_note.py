"""Module that contains Note class tests."""
import pytest
from backend.models import Note
from backend.utils.enums import BackgroundColor
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError


def test_note_valid():
    """Tests valid note."""
    note = Note(
        title="test",
        content="test",
        background_color=BackgroundColor.BLUE
    )

    assert isinstance(note.title, str)
    assert note.title == "test"
    assert isinstance(note.content, str)
    assert note.content == "test"
    assert isinstance(note.background_color, BackgroundColor)
    assert note.background_color == BackgroundColor.BLUE


def tests_note_to_dict(note):
    """Tests to_dict."""
    expected = {
        "title": "test",
        "content": "test",
        "background_color": "BLUE",
    }

    d = note.to_dict()
    for key, value in expected.items():
        assert d[key] == value


def test_note_missing_content_raises(app):
    """Tests note with missing content."""
    note = Note(
        title="test",
        background_color=BackgroundColor.BLUE,
    )
    with pytest.raises(IntegrityError):
        note.save()


def test_note_title_too_long(app):
    """Tests note with a long title raises value error."""
    with pytest.raises(
        ValidationError,
        match="between 3 and 30 characters"
    ):
        Note(
            title="a"*32,
            content="content",
            background_color=BackgroundColor.BLUE
        )


def test_note_title_too_short(app):
    """Tests note with a short title raises value error."""
    with pytest.raises(
        ValidationError,
        match="between 3 and 30 characters"
    ):
        Note(
            title="aa",
            content="content",
            background_color=BackgroundColor.BLUE
        )

"""Module that contains Habit schema tests."""
import pytest
from backend.schemas.habit_schema import HabitSchema
from marshmallow import ValidationError
from datetime import date

habit_schema = HabitSchema()


def test_valid_habit_schema():
    """Tests valid habit schema."""
    data = {
        "title": "test",
        "description": "test",
        "frequency": "WEEKLY",
        "target_count": 1,
        "current_streak": 5,
        "longest_streak": 10,
        "last_completed": "2025-07-09",
        "priority": "HIGH",
        "category": "WORK",
        "is_active": True,
        "background_color": "BLUE"
    }
    loaded = habit_schema.load(data)

    assert loaded["title"] == "test"
    assert loaded["description"] == "test"
    assert loaded["frequency"] == "WEEKLY"
    assert loaded["target_count"] == 1
    assert loaded["current_streak"] == 5
    assert loaded["longest_streak"] == 10
    assert loaded["last_completed"] == date(2025, 7, 9)
    assert loaded["priority"] == "HIGH"
    assert loaded["category"] == "WORK"
    assert loaded["is_active"] is True
    assert loaded["background_color"] == "BLUE"


def test_invalid_habit_schema():
    """Tests invalid habit schema."""
    data = {
        "frequency": "INVALID_FREQUENCY",
        "priority": "INVALID_PRIORITY",
        "category": "INVALID_CATEGORY"
    }
    with pytest.raises(ValidationError) as e:
        habit_schema.load(data)

    assert "title" in e.value.messages
    assert "frequency" in e.value.messages
    assert "target_count" in e.value.messages
    assert "priority" in e.value.messages
    assert "category" in e.value.messages

    assert "description" not in e.value.messages
    assert "current_streak" not in e.value.messages
    assert "longest_streak" not in e.value.messages
    assert "last_completed" not in e.value.messages
    assert "is_active" not in e.value.messages
    assert "background_color" not in e.value.messages


def test_habit_schema_title_too_short():
    """Tests habit schema title too short."""
    data = {
        "title": "aa",
    }
    with pytest.raises(ValidationError) as e:
        habit_schema.load(data)
    assert "title" in e.value.messages


def test_habit_schema_title_too_long():
    """Tests habit title too long."""
    data = {
        "title": "a" * 31,
    }
    with pytest.raises(ValidationError) as e:
        habit_schema.load(data)
    assert "title" in e.value.messages

"""Module that contains Task schema tests."""
import pytest
from backend.schemas.task_schema import TaskSchema
from marshmallow import ValidationError
from datetime import date, datetime

task_schema = TaskSchema()


def test_valid_task_schema():
    """Tests valid task schema."""
    data = {
        "title": "test",
        "description": "test",
        "priority": "HIGH",
        "category": "WORK",
        "deadline": "2025-06-30",
        "completed": False,
        "completed_at": "2025-06-30 18:30:02"
    }
    loaded = task_schema.load(data)

    assert loaded["title"] == "test"
    assert loaded["description"] == "test"
    assert loaded["priority"] == "HIGH"
    assert loaded["category"] == "WORK"
    assert loaded["deadline"] == date(2025, 6, 30)
    assert loaded["completed"] is False
    assert loaded["completed_at"] == datetime(2025, 6, 30, 18, 30, 2)


def test_invalid_task_schema():
    """Tests invalid task schema."""
    data = {
        "priority": "INVALID_PRIORITY",
        "category": "INVALID_CATEGORY"
    }
    with pytest.raises(ValidationError) as e:
        task_schema.load(data)

    assert "title" in e.value.messages
    assert "description" in e.value.messages
    assert "priority" in e.value.messages
    assert "category" in e.value.messages
    assert "deadline" in e.value.messages

    assert "completed" not in e.value.messages
    assert "completed_at" not in e.value.messages


def test_task_schema_title_too_short():
    """Tests task schema title too short."""
    data = {
        "title": "aa",
    }
    with pytest.raises(ValidationError) as e:
        task_schema.load(data)
    assert "title" in e.value.messages


def test_task_schema_title_too_long():
    """Tests task title too long."""
    data = {
        "title": "a" * 31,
    }
    with pytest.raises(ValidationError) as e:
        task_schema.load(data)
    assert "title" in e.value.messages

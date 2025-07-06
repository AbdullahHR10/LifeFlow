"""Module that contains Task class tests."""
import pytest
from backend.models import Task
from backend.utils.enums import Priority, Category
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError


def test_task_valid():
    """Tests valid task."""
    task = Task(
        title="test",
        description="test",
        priority=Priority.HIGH,
        deadline=date(2025, 6, 30),
        completed=True,
        category=Category.WORK,
        completed_at=datetime(2025, 6, 30, 18, 30, 2),
    )

    assert isinstance(task.title, str)
    assert task.title == "test"
    assert isinstance(task.description, str)
    assert task.description == "test"
    assert isinstance(task.priority, Priority)
    assert task.priority == Priority.HIGH
    assert isinstance(task.deadline, date)
    assert task.deadline == date(2025, 6, 30)
    assert isinstance(task.completed, bool)
    assert task.completed is True
    assert isinstance(task.category, Category)
    assert task.category == Category.WORK
    assert isinstance(task.completed_at, datetime)
    assert task.completed_at == datetime(2025, 6, 30, 18, 30, 2)


def test_mark_complete_sets_completed_and_timestamp(task):
    """Test mark_complete sets completed=True and completed_at to datetime."""
    before = datetime.now()
    task.mark_complete()
    after = datetime.now()

    assert task.completed is True
    assert isinstance(task.completed_at, datetime)
    assert before <= task.completed_at <= after


def test_mark_incomplete_sets_completed_false_and_nulls_timestamp(task):
    """Test mark_incomplete sets completed=False and completed_at=None."""
    task.completed = True
    task.completed_at = datetime.now()
    task.mark_incomplete()

    assert task.completed is False
    assert task.completed_at is None


def tests_task_to_dict(task):
    """Tests to_dict handles enum and date values."""
    expected = {
        "title": "test",
        "description": "test",
        "priority": "HIGH",
        "category": "WORK",
        "deadline": "2025-06-30",
        "completed": True,
        "completed_at": "2025-06-30 18:30:02"
    }

    d = task.to_dict()
    for key, value in expected.items():
        assert d[key] == value


def test_task_missing_description_raises(app):
    """Tests task with missing description."""
    task = Task(
        title="test",
        priority=Priority.HIGH,
        deadline=date.today(),
        completed=False,
        category=Category.WORK,
        user_id="some-user-id"
    )
    with pytest.raises(IntegrityError):
        task.save()


def test_task_title_too_long(app):
    """Tests task with a long title raises value error."""
    with pytest.raises(
        ValidationError, 
        match="between 3 and 30 characters"
    ):
        Task(
            title="a"*32,
            description="desc",
            priority=Priority.HIGH,
            deadline=date.today(),
            completed=False,
            category=Category.WORK,
            user_id="some-user-id"
        )

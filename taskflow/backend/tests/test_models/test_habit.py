"""Module that contains Habit class tests."""
import pytest
from backend.models import Habit
from backend.utils.enums import Frequency, Priority, Category, BackgroundColor
from datetime import datetime, date, timedelta
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError


def test_habit_valid():
    """Tests valid habit."""
    habit = Habit(
        title="test",
        description="test",
        frequency=Frequency.DAILY,
        target_count=1,
        current_streak=1,
        longest_streak=1,
        last_completed=date(2025, 5, 1),
        priority=Priority.HIGH,
        category=Category.WORK,
        is_active=True,
        background_color=BackgroundColor.BLUE,
    )

    assert isinstance(habit.title, str)
    assert habit.title == "test"
    assert isinstance(habit.description, str)
    assert habit.description == "test"
    assert isinstance(habit.frequency, Frequency)
    assert habit.frequency == Frequency.DAILY
    assert isinstance(habit.target_count, int)
    assert habit.target_count == 1
    assert isinstance(habit.current_streak, int)
    assert habit.current_streak == 1
    assert isinstance(habit.longest_streak, int)
    assert habit.longest_streak == 1
    assert isinstance(habit.last_completed, date)
    assert habit.last_completed == date(2025, 5, 1)
    assert isinstance(habit.priority, Priority)
    assert habit.priority == Priority.HIGH
    assert isinstance(habit.category, Category)
    assert habit.category == Category.WORK
    assert isinstance(habit.is_active, bool)
    assert habit.is_active is True
    assert isinstance(habit.background_color, BackgroundColor)
    assert habit.background_color == BackgroundColor.BLUE


def test_mark_complete(habit):
    """Test mark_complete."""
    habit.last_completed = date.today() - timedelta(days=1)
    habit.current_streak = 3
    streak_before = habit.current_streak
    habit.mark_complete()

    assert habit.current_streak == streak_before + 1
    assert isinstance(habit.last_completed, date)
    assert habit.last_completed == date.today()


def tests_habit_to_dict(habit):
    """Tests to_dict handles enum and date values."""
    expected = {
        "title": "test",
        "description": "test",
        "frequency": "DAILY",
        "target_count": 1,
        "current_streak": 1,
        "longest_streak": 1,
        "last_completed": "2025-05-01",
        "priority": "HIGH",
        "category": "WORK",
        "is_active": True,
        "background_color": "BLUE",
    }

    d = habit.to_dict()
    for key, value in expected.items():
        assert d[key] == value


def test_habit_missing_description_raises(app):
    """Tests habit with missing description."""
    habit = Habit(
        title="test",
        frequency=Frequency.DAILY,
        target_count=1,
        current_streak=1,
        longest_streak=1,
        last_completed=date(2025, 5, 1),
        priority=Priority.HIGH,
        category=Category.WORK,
        is_active=True,
        background_color=BackgroundColor.BLUE,
    )
    with pytest.raises(IntegrityError):
        habit.save()


def test_habit_title_too_long(app):
    """Tests habit with a long title raises value error."""
    with pytest.raises(
        ValidationError,
        match="between 3 and 30 characters"
    ):
        Habit(
            title="a"*32,
            description="desc",
            priority=Priority.HIGH,
            deadline=date.today(),
            completed=False,
            category=Category.WORK,
            user_id="some-user-id"
        )


def test_mark_complete_already_completed(habit):
    """Test that completing a habit twice in the same day raises."""
    habit.last_completed = date.today()
    with pytest.raises(ValueError, match="already completed"):
        habit.mark_complete()


def test_mark_complete_resets_streak(habit):
    """Test mark_complete resets streak when last_completed is older."""
    habit.last_completed = date.today() - timedelta(days=3)
    habit.current_streak = 5

    habit.mark_complete()

    assert habit.current_streak == 1
    assert habit.last_completed == date.today()


def test_habit_title_too_short(app):
    """Tests habit with a short title raises value error."""
    with pytest.raises(
        ValidationError,
        match="between 3 and 30 characters"
    ):
        Habit(
            title="aa",
            description="desc",
            priority=Priority.HIGH,
            deadline=date.today(),
            completed=False,
            category=Category.WORK,
            user_id="some-user-id"
        )

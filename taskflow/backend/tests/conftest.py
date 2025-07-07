"""Moudle that contains shared fixtures, hooks, and config for pytest."""

import pytest
from backend import create_app, db
from backend.models import User, Task, Habit, Note
from backend.utils.enums import Frequency, Priority, Category, BackgroundColor
from datetime import datetime, date


@pytest.fixture
def app():
    """Sets up Flask app for each test."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Returns a Flask test client."""
    return app.test_client()


@pytest.fixture
def user(app):
    """User instance."""
    user = User(
        name="testuser",
        email="testemail@example.com",
    )
    user.password = "123456"
    user.save(refresh=True)
    return user


@pytest.fixture
def task(app, user):
    """Task instance."""
    task = Task(
        title="test",
        description="test",
        priority=Priority.HIGH,
        deadline=date(2025, 6, 30),
        completed=True,
        category=Category.WORK,
        completed_at=datetime(2025, 6, 30, 18, 30, 2),
        user_id=user.id
    )
    task.save(refresh=True)
    return task


@pytest.fixture
def note(app, user):
    """Note instance."""
    note = Note(
        title="test",
        content="test",
        background_color=BackgroundColor.BLUE,
        user_id=user.id
    )
    note.save(refresh=True)
    return note


@pytest.fixture
def habit(app, user):
    """Habit instance."""
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
        user_id=user.id
    )
    habit.save(refresh=True)
    return habit


@pytest.fixture
def logged_in_client(client, user):
    with client:
        client.post("/auth/v1/login", json={
            "email": user.email,
            "password": "123456"
        })
        yield client

"""Moudle that contains shared fixtures, hooks, and config for pytest."""

import pytest
from backend import create_app, db
from backend.models import User, Task
from backend.utils.enums import Priority, Category
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
    user = User(
        name="testuser",
        email="testemail@example.com",
    )
    user.password = "123456"
    user.save()
    return user


@pytest.fixture
def user(app):
    user = User(
        name="testuser",
        email="testemail@example.com",
    )
    user.password = "123456"
    user.save(refresh=True)
    return user


@pytest.fixture
def task(app, user):
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
def logged_in_client(client, user):
    with client:
        client.post("/auth/v1/login", json={
            "email": user.email,
            "password": "123456"
        })
        yield client

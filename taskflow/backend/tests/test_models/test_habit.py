"""Module that contains the Habit class unittests."""

import unittest
from backend import create_app, db
from backend.models.user import User
from backend.models.habit import Habit
from backend.utils.enums import BackgroundColor, Priority, Category
from datetime import datetime, date


class TestHabitClass(unittest.TestCase):
    """Unit tests for the Habit model."""
    def setUp(self):
        """Sets up the flask app and database for all tests."""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.user = User(
            name="testuser",
            email="testemail@example.com"
        )
        self.habit = Habit(
            title="Test habit",
            description="Test habit description",
            frequency=1,
            target_count=1,
            current_streak=1,
            longest_streak=1,
            last_completed=date(2025, 5, 1),
            priority=Priority.HIGH,
            category=Category.WORK,
            is_active=True,
            background_color=BackgroundColor.BLUE,
            user_id=self.user.id
        )

    def tearDown(self):
        """Tears down the Flask app and database after the tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_id(self):
        """Tests that the habit's id is correct."""
        self.assertIsInstance(self.habit.id, str)

    def test_created_at(self):
        """Tests the habit's created_at if it's correct."""
        self.assertIsInstance(self.habit.created_at, datetime)

    def test_updated_at(self):
        """Tests the habit's updated_at if it's correct."""
        self.assertIsInstance(self.habit.updated_at, datetime)

    def test_title(self):
        """Tests the habit's title if it's correct."""
        self.assertIsInstance(self.habit.title, str)
        self.assertEqual(self.habit.title, "Test habit")

    def test_description(self):
        """Tests the habit's description if it's correct."""
        self.assertIsInstance(self.habit.description, str)
        self.assertEqual(self.habit.description, "Test habit description")

    def test_background_color(self):
        """Tests the habit's category if it's correct."""
        self.assertIsInstance(self.habit.background_color, str)
        self.assertEqual(self.habit.background_color, "Blue")
        self.assertEqual(self.habit.background_color,
                         BackgroundColor.BLUE.value)

    def test_save_method(self):
        """Tests that the save method adds and commits
        the habit instance to the database."""
        self.habit.priority = Priority.HIGH
        self.habit.category = Category.WORK
        self.habit.background_color = BackgroundColor.BLUE
        self.habit.save()
        retrived = db.session.get(Habit, self.habit.id)
        self.assertIsNotNone(retrived)
        self.assertEqual(retrived.title, self.habit.title)
        self.assertEqual(retrived.description, self.habit.description)
        self.assertEqual(retrived.background_color,
                         self.habit.background_color)

    def test_delete_method(self):
        """Tests that the delete method removes
        the habit instance from the database."""
        self.habit.priority = Priority.HIGH
        self.habit.category = Category.WORK
        self.habit.background_color = BackgroundColor.BLUE
        self.habit.save()
        self.habit.delete()
        retrived = db.session.get(Habit, self.habit.id)
        self.assertIsNone(retrived)

    def test_to_dict_method(self):
        """Tests that the to_dict method returns a dict
        with object attributes."""
        expected_dict = {
            "id": self.habit.id,
            "created_at": self.habit.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.habit.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            "title": "Test habit",
            "description": "Test habit description",
            "frequency": 1,
            "target_count": 1,
            "current_streak": 1,
            "longest_streak": 1,
            "last_completed": self.habit.last_completed.strftime(
                '%Y-%m-%d') if self.habit.last_completed else None,
            "priority": Priority.HIGH.value,
            "category": Category.WORK.value,
            "is_active": True,
            "background_color": BackgroundColor.BLUE.value,
            "user_id": self.user.id
        }
        self.assertEqual(self.habit.to_dict(), expected_dict)

    def test_str_method(self):
        """Tests that the __str__ method returns a
        string representation of the object."""
        dict_rep = self.habit.to_dict()
        expected_str = f"[Habit] ({self.habit.id}) {dict_rep}"
        self.assertEqual(self.habit.__str__(), expected_str)


if __name__ == "__main__":
    unittest.main()

"""Module that contains the Habit class unittests."""

import unittest
from backend.tests.base_test import BaseTestCase
from backend import db
from backend.models.habit import Habit, Frequency
from backend.utils.enums import BackgroundColor, Priority, Category
from datetime import datetime, date


class TestHabitClass(BaseTestCase):
    """Unit tests for the Habit model."""
    def setUp(self):
        """Extends setup with additional test-specific configurations."""
        super().setUp(user=True)
        self.habit = Habit(
            title="Test habit",
            description="Test habit description",
            frequency=Frequency.DAILY,
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

    def test_frequency(self):
        """Tests the habit's frequency if it's correct."""
        self.assertIsInstance(self.habit.frequency, Frequency)
        self.assertEqual(self.habit.frequency.name, "DAILY")
        self.assertEqual(self.habit.frequency.value, "Daily")

    def test_target_count(self):
        """Tests the habit's target_count if it's correct."""
        self.assertIsInstance(self.habit.target_count, int)
        self.assertEqual(self.habit.target_count, 1)

    def test_current_streak(self):
        """Tests the habit's current_streak if it's correct."""
        self.assertIsInstance(self.habit.current_streak, int)
        self.assertEqual(self.habit.current_streak, 1)

    def test_longest_streak(self):
        """Tests the habit's longest_streak if it's correct."""
        self.assertIsInstance(self.habit.longest_streak, int)
        self.assertEqual(self.habit.longest_streak, 1)

    def test_last_completed(self):
        """Tests the habit's last_completed if it's correct."""
        self.assertIsInstance(self.habit.last_completed, date)
        self.assertEqual(self.habit.last_completed, date(2025, 5, 1))

    def test_priority(self):
        """Tests the habit's priority if it's correct."""
        self.assertIsInstance(self.habit.priority, Priority)
        self.assertEqual(self.habit.priority.name, "HIGH")
        self.assertEqual(self.habit.priority.value, "High")

    def test_category(self):
        """Tests the habit's category if it's correct."""
        self.assertIsInstance(self.habit.category, Category)
        self.assertEqual(self.habit.category.name, "WORK")
        self.assertEqual(self.habit.category.value, "Work")

    def test_is_active(self):
        """Tests the habit's is_active if it's correct."""
        self.assertIsInstance(self.habit.is_active, bool)
        self.assertEqual(self.habit.is_active, True)

    def test_background_color(self):
        """Tests the habit's category if it's correct."""
        self.assertIsInstance(self.habit.background_color, BackgroundColor)
        self.assertEqual(self.habit.background_color.name, "BLUE")
        self.assertEqual(self.habit.background_color.value, "Blue")

    def test_save_method(self):
        """Tests that the save method adds and commits
        the habit instance to the database."""
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
            "frequency": "DAILY",
            "target_count": 1,
            "current_streak": 1,
            "longest_streak": 1,
            "last_completed": self.habit.last_completed.strftime('%Y-%m-%d'),
            "priority": "HIGH",
            "category": "WORK",
            "is_active": True,
            "background_color": "BLUE",
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

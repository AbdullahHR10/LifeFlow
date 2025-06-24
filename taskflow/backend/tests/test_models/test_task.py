"""Module that contains the Task class unittests."""

import unittest
from backend.tests.base_test import BaseTestCase
from backend import db
from backend.models.task import Task
from backend.utils.enums import Category, Priority
from datetime import datetime, date


class TestTaskClass(BaseTestCase):
    """Unit tests for the Task model."""
    def setUp(self):
        """Extends setup with additional test-specific configurations."""
        super().setUp()
        self.task = Task(
            title="Test task",
            description="Test task description",
            priority=Priority.HIGH,
            deadline=date(2025, 5, 1),
            completed=False,
            category=Category.WORK,
            user_id=self.user.id
        )

    def test_id(self):
        """Tests that the task's id is correct."""
        self.assertIsInstance(self.task.id, str)

    def test_created_at(self):
        """Tests the task's created_at if it's correct."""
        self.assertIsInstance(self.task.created_at, datetime)

    def test_updated_at(self):
        """Tests the task's updated_at if it's correct."""
        self.assertIsInstance(self.task.updated_at, datetime)

    def test_title(self):
        """Tests the task's title if it's correct."""
        self.assertIsInstance(self.task.title, str)
        self.assertEqual(self.task.title, "Test task")

    def test_description(self):
        """Tests the task's description if it's correct."""
        self.assertIsInstance(self.task.description, str)
        self.assertEqual(self.task.description, "Test task description")

    def test_priority(self):
        """Tests the task's priority if it's correct."""
        self.assertIsInstance(self.task.priority, Priority)
        self.assertEqual(self.task.priority.name, "HIGH")
        self.assertEqual(self.task.priority.value, "High")

    def test_deadline(self):
        """Tests the task's priority if it's correct."""
        self.assertIsInstance(self.task.deadline, date)
        self.assertEqual(self.task.deadline, date(2025, 5, 1))

    def test_not_completed(self):
        """Tests the task's completed if it's not completed."""
        self.assertIsInstance(self.task.completed, bool)
        self.assertEqual(self.task.completed, False)

    def test_category(self):
        """Tests the task's category if it's correct."""
        self.assertIsInstance(self.task.category, Category)
        self.assertEqual(self.task.category.name, "WORK")
        self.assertEqual(self.task.category.value, "Work")

    def test_completed_task_methods(self):
        """Tests the mark_complete and mark_incomplete methods."""
        self.task.mark_complete()
        self.assertTrue(self.task.completed)
        self.task.mark_incomplete()
        self.assertFalse(self.task.completed)

    def test_save_method(self):
        """Tests that the save method adds and commits
        the task instance to the database."""
        self.task.save()
        retrived = db.session.get(Task, self.task.id)
        self.assertIsNotNone(retrived)
        self.assertEqual(retrived.title, self.task.title)
        self.assertEqual(retrived.description, self.task.description)
        self.assertEqual(retrived.priority, self.task.priority)
        self.assertEqual(retrived.deadline, self.task.deadline)
        self.assertEqual(retrived.completed, self.task.completed)
        self.assertEqual(retrived.category, self.task.category)

    def test_delete_method(self):
        """Tests that the delete method removes
        the task instance from the database."""
        self.task.save()
        self.task.delete()
        retrived = db.session.get(Task, self.task.id)
        self.assertIsNone(retrived)

    def test_to_dict_method(self):
        """Tests that the to_dict method returns a dict
        with object attributes."""
        expected_dict = {
            "id": self.task.id,
            "created_at": self.task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.task.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            "title": "Test task",
            "description": "Test task description",
            "priority": "HIGH",
            "deadline": "2025-05-01",
            "completed": False,
            "category": "WORK",
            "user_id": self.user.id
        }
        self.assertEqual(self.task.to_dict(), expected_dict)

    def test_str_method(self):
        """Tests that the __str__ method returns a
        string representation of the object."""
        dict_rep = self.task.to_dict()
        expected_str = f"[Task] ({self.task.id}) {dict_rep}"
        self.assertEqual(self.task.__str__(), expected_str)


if __name__ == "__main__":
    unittest.main()

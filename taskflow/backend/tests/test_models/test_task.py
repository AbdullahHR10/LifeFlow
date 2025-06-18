"""Module that contains the Task class unittests."""

import unittest
from backend import create_app, db
from backend.models.user import User
from backend.models.task import Task, Priority, Category
from datetime import date


class TestTaskClass(unittest.TestCase):
    """Unit tests for the Task model."""
    def setUp(self):
        """Sets up the flask app and database for all tests."""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.user = User(
            id="f47ac10b-58cc-4372-a567-0e02b2c3d479",
            created_at="2025-05-01 22:00:00",
            updated_at="2025-05-02 18:12:00",
            name="testuser",
            email="testemail@example.com"
        )
        self.task = Task(
            id="f47ac10b-58cc-4372-a567-0e02b2c3d479",
            created_at="2025-05-01 22:00:00",
            updated_at="2025-05-02 18:12:00",
            title="Test task",
            description="Test task description",
            priority=Priority.HIGH,
            deadline=date(2025, 5, 1),
            completed=False,
            category=Category.WORK,
            user_id=self.user.id
        )

    def tearDown(self):
        """Tears down the Flask app and database after the tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_id(self):
        """Tests that the task's id is correct."""
        self.assertIsInstance(self.task.id, str)
        self.assertEqual(self.task.id, "f47ac10b-58cc-4372-a567-0e02b2c3d479")

    def test_created_at(self):
        """Tests the task's created_at if it's correct."""
        self.assertIsInstance(self.task.created_at, str)
        self.assertEqual(self.task.created_at, "2025-05-01 22:00:00")

    def test_updated_at(self):
        """Tests the task's updated_at if it's correct."""
        self.assertIsInstance(self.task.updated_at, str)
        self.assertEqual(self.task.updated_at, "2025-05-02 18:12:00")

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
        self.assertIsInstance(self.task.priority, str)
        self.assertEqual(self.task.priority, "High")
        self.assertEqual(self.task.priority, Priority.HIGH.value)

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
        self.assertIsInstance(self.task.category, str)
        self.assertEqual(self.task.category, "Work")
        self.assertEqual(self.task.category, Category.WORK.value)

    def test_completed_task_methods(self):
        """Tests the mark_complete and mark_incomplete methods."""
        self.task.priority = Priority.HIGH
        self.task.category = Category.WORK
        self.task.mark_complete()
        self.assertTrue(self.task.completed)
        self.task.mark_incomplete()
        self.assertFalse(self.task.completed)

    def test_save_method(self):
        """Tests that the save method adds and commits
        the task instance to the database."""
        self.task.priority = Priority.HIGH
        self.task.category = Category.WORK
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
        self.task.priority = Priority.HIGH
        self.task.category = Category.WORK
        self.task.save()
        self.task.delete()
        retrived = db.session.get(Task, self.task.id)
        self.assertIsNone(retrived)

    def test_to_dict_method(self):
        """Tests that the to_dict method returns a dict
        with object attributes."""
        expected_dict = {
            "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "created_at": "2025-05-01 22:00:00",
            "updated_at": "2025-05-02 18:12:00",
            "title": "Test task",
            "description": "Test task description",
            "priority": Priority.HIGH.value,
            "deadline": "2025-05-01",
            "completed": False,
            "category": Category.WORK.value,
            "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
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

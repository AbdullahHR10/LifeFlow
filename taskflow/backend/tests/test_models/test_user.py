"""Module that contains the User class unittests."""

import unittest
from backend import create_app, db
from backend.models.user import User
from datetime import datetime


class TestUserClass(unittest.TestCase):
    """Unittest Class that tests the User class."""
    def setUp(self):
        """Sets up the Flask app and database for all tests."""
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
            email="testemail@example.com",
        )
        self.user.password = "123456"

    def tearDown(self):
        """Tears down the Flask app and database after the tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_id(self):
        """Tests the User class's id"""
        self.assertIsInstance(self.user.id, str)
        self.assertEqual(self.user.id, "f47ac10b-58cc-4372-a567-0e02b2c3d479")

    def test_created_at(self):
        """Tests the User class's created_at"""
        self.assertIsInstance(self.user.created_at, str)
        self.assertEqual(self.user.created_at, "2025-05-01 22:00:00")

    def test_updated_at(self):
        """Tests the User class's updated_at"""
        self.assertIsInstance(self.user.updated_at, str)
        self.assertEqual(self.user.updated_at, "2025-05-02 18:12:00")

    def test_name(self):
        """Tests the User class's name"""
        self.assertIsInstance(self.user.name, str)
        self.assertEqual(self.user.name, "testuser")

    def test_name_long(self):
        """Tests the User class's name if it's too long."""
        with self.assertRaises(ValueError) as context:
            self.user.name = "a" * 31
        self.assertIn("name must be between 3 and 30 characters", str(context.exception))

    def test_name_short(self):
        """Tests the User class's name if it's too short."""
        with self.assertRaises(ValueError) as context:
            self.user.name = "aa"
        self.assertIn("name must be between 3 and 30 characters", str(context.exception))

    def test_email(self):
        """Tests the User class's email"""
        self.assertIsInstance(self.user.email, str)
        self.assertEqual(self.user.email, "testemail@example.com")

    def test_password(self):
        """Tests the User class's password"""
        self.assertIsInstance(self.user._password, str)
        self.assertTrue(self.user.check_password("123456"))
        self.assertFalse(self.user.check_password("wrongpassword"))
        self.assertNotEqual(self.user._password, "123456")


if __name__ == "__main__":
    unittest.main()

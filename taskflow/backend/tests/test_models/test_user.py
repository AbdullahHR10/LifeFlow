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

    def test_attributes(self):
        """Tests the User class's attributes"""
        self.assertIsInstance(self.user.id, str)
        self.assertEqual(self.user.id, "f47ac10b-58cc-4372-a567-0e02b2c3d479")

        self.assertIsInstance(self.user.created_at, str)
        self.assertEqual(self.user.created_at, "2025-05-01 22:00:00")

        self.assertIsInstance(self.user.updated_at, str)
        self.assertEqual(self.user.updated_at, "2025-05-02 18:12:00")

        self.assertIsInstance(self.user.name, str)
        self.assertEqual(self.user.name, "testuser")

        self.assertIsInstance(self.user.email, str)
        self.assertEqual(self.user.email, "testemail@example.com")

        self.assertIsInstance(self.user._password, str)
        self.assertTrue(self.user.check_password("123456"))
        self.assertFalse(self.user.check_password("wrongpassword"))


if __name__ == "__main__":
    unittest.main()

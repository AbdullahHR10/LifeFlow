"""Module that contains the User class unittests."""

import unittest
from backend import create_app, db
from backend.models.user import User


class TestUserClass(unittest.TestCase):
    """Unit tests for the User model."""
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
        """Tests that the user's id is correct."""
        self.assertIsInstance(self.user.id, str)
        self.assertEqual(self.user.id, "f47ac10b-58cc-4372-a567-0e02b2c3d479")

    def test_created_at(self):
        """Tests the user's created_at if it's correct."""
        self.assertIsInstance(self.user.created_at, str)
        self.assertEqual(self.user.created_at, "2025-05-01 22:00:00")

    def test_updated_at(self):
        """Tests the user's updated_at if it's correct."""
        self.assertIsInstance(self.user.updated_at, str)
        self.assertEqual(self.user.updated_at, "2025-05-02 18:12:00")

    def test_valid_name(self):
        """Tests that a valid name passes validation."""
        self.assertIsInstance(self.user.name, str)
        self.assertEqual(self.user.name, "testuser")

    def test_name_if_too_long(self):
        """
        Tests the user's name if it's too long.

        Raises:
            ValueError: if the name is too long.
        """
        with self.assertRaises(ValueError) as context:
            self.user.name = "a" * 31
        self.assertIn("name must be between 3 and 30 characters", str(context.exception))

    def test_name_if_too_short(self):
        """
        Tests the user's name if it's too short.

        Raises:
            ValueError: if the name is too short.
        """
        with self.assertRaises(ValueError) as context:
            self.user.name = "aa"
        self.assertIn("name must be between 3 and 30 characters", str(context.exception))

    def test_valid_email(self):
        """Tests that a valid email passes validation."""
        try:
            self.user.email = "valid.email@example.com"
        except ValueError:
            self.fail("Valid email raised ValueError unexpectedly.")

    def test_email_must_have_exactly_one_at_symbol(self):
        """
        Tests the user's email when it lacks exactly one '@' symbol.

        Raises:
            ValueError: If the email does not contain exactly one '@' character.
        """
        with self.assertRaises(ValueError) as context:
            self.user.email = "aa"
        self.assertIn("email must contain exactly one '@' character.", str(context.exception))

    def test_email_cannot_start_or_end_with_at(self):
        """
        Tests the user's email when it starts or ends with '@'.

        Raises:
            ValueError: If the email starts or ends with '@'.
        """
        with self.assertRaises(ValueError) as context:
            self.user.email = "@"
        self.assertIn("email cannot start or end with '@'.", str(context.exception))

    def test_email_cannot_start_or_end_with_dot(self):
        """
        Tests the user's email when it starts or ends with '.'.

        Raises:
            ValueError: If the email starts or ends with '.'.
        """
        with self.assertRaises(ValueError) as context:
            self.user.email = "a@."
        self.assertIn("email cannot start or end with '.'.", str(context.exception))

    def test_email_cannot_contain_consecutive_dots(self):
        """
        Tests the user's email when it contains consecutive dots ('..').

        Raises:
            ValueError: If the email contains consecutive dots ('..').
        """
        with self.assertRaises(ValueError) as context:
            self.user.email = "a@..com"
        self.assertIn("email cannot contain consecutive dots ('..').", str(context.exception))

    def test_email_must_have_dot_after_at(self):
        """
        Tests the user's email when there is no '.' after the '@'.

        Raises:
            ValueError: If the email lacks a dot ('.') after the '@'.
        """
        with self.assertRaises(ValueError) as context:
            self.user.email = "a.a@com"
        self.assertIn("email must contain a dot ('.') after the '@'.", str(context.exception))

    def test_password_hashing_and_validation(self):
        """Tests that the user's password is hashed and validated correctly."""
        self.assertTrue(self.user.check_password("123456"))
        self.assertFalse(self.user.check_password("wrongpassword"))
        self.assertNotEqual(self.user._password, "123456")

    def test_password_getter_raises_error(self):
        """Tests that accessing raw password raises AttributeError."""
        with self.assertRaises(AttributeError):
            _ = self.user.password

if __name__ == "__main__":
    unittest.main()

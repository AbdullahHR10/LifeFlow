"""Module that contains the User class unittests."""

import unittest
from backend.tests.base_test import BaseTestCase
from backend import db
from backend.models.user import User
import logging
from backend.utils.logger import logger
from datetime import datetime


class TestUserClass(BaseTestCase):
    """Unit tests for the User model."""
    def setUp(self):
        """Extends setup with additional test-specific configurations."""
        super().setUp()
        self.user.password = "123456"
        self._original_log_level = logger.level
        logger.setLevel(logging.CRITICAL)

    def tearDown(self):
        """Restores the original logger level after tests."""
        logger.setLevel(self._original_log_level)

    def test_id(self):
        """Tests that the user's id is correct."""
        self.assertIsInstance(self.user.id, str)

    def test_created_at(self):
        """Tests the user's created_at if it's correct."""
        self.assertIsInstance(self.user.created_at, datetime)

    def test_updated_at(self):
        """Tests the user's updated_at if it's correct."""
        self.assertIsInstance(self.user.updated_at, datetime)

    def test_valid_name(self):
        """Tests that a valid name passes validation."""
        self.assertIsInstance(self.user.name, str)
        self.assertEqual(self.user.name, "testuser")

    def test_name_if_too_long(self):
        """Tests that setting the user's name too long raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            self.user.name = "a" * 31
        self.assertIn("name must be between 3 and 30 characters",
                      str(context.exception))

    def test_name_if_too_short(self):
        """Tests that setting the user's name too short
        raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            self.user.name = "aa"
        self.assertIn("name must be between 3 and 30 characters",
                      str(context.exception))

    def test_valid_email(self):
        """Tests that a valid email passes validation."""
        try:
            self.user.email = "valid.email@example.com"
        except ValueError:
            self.fail("Valid email raised ValueError unexpectedly.")

    def test_unique_email(self):
        """
        Verifies that cloning a user with a unique email
        successfully creates and saves a new user.
        """
        user_2 = User(
            name="testuser",
            email="unique@example.com"
        )
        user_2.password = "abcdef"
        user_2.save()
        self.assertIsNotNone(user_2.id)
        self.assertIsNotNone(user_2)
        self.assertEqual(user_2.email, "unique@example.com")

    def test_not_unique_email(self):
        """
        Verifies that cloning a user with a duplicate email
        raises an ValueError upon saving.
        """
        self.user.save()
        clone = User(
            name="testuser",
            email="testemail@example.com",
        )
        clone.password = "654321"
        from sqlalchemy.exc import IntegrityError
        with self.assertRaises(IntegrityError) as context:
            clone.save()
            self.assertIn(
                f"'email' value '{self.user.email}' already exists. "
                f"Must provide a unique value.",
                str(context.exception)
            )

    def test_email_must_have_exactly_one_at_symbol(self):
        """Tests that setting an email without exactly one '@'
        character raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            self.user.email = "aa"
        self.assertIn("email must contain exactly one '@' character.",
                      str(context.exception))

    def test_email_cannot_start_or_end_with_at(self):
        """Tests that setting an email starting or ending with '@'
        raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            self.user.email = "@"
        self.assertIn("email cannot start or end with '@'.",
                      str(context.exception))

    def test_email_cannot_start_or_end_with_dot(self):
        """Tests that setting an email starting or ending with '.'
        raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            self.user.email = "a@."
        self.assertIn("email cannot start or end with '.'.",
                      str(context.exception))

    def test_email_cannot_contain_consecutive_dots(self):
        """Tests that setting an email containing consecutive dots ('..')
        raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            self.user.email = "a@..com"
        self.assertIn("email cannot contain consecutive dots ('..').",
                      str(context.exception))

    def test_email_must_have_dot_after_at(self):
        """Tests that setting an email lacking a dot ('.') after the '@'
        raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            self.user.email = "a.a@com"
        self.assertIn("email must contain a dot ('.') after the '@'.",
                      str(context.exception))

    def test_password_hashing_and_validation(self):
        """Tests that the user's password is hashed
        and validated correctly."""
        self.assertTrue(self.user.check_password("123456"))
        self.assertFalse(self.user.check_password("wrongpassword"))
        self.assertNotEqual(self.user._password, "123456")

    def test_password_getter_raises_error(self):
        """Tests that accessing raw password raises AttributeError."""
        with self.assertRaises(AttributeError):
            _ = self.user.password

    def test_save_method(self):
        """Tests that the save method adds and commits
        the user instance to the database."""
        self.user.save()
        retrived = db.session.get(User, self.user.id)
        self.assertIsNotNone(retrived)
        self.assertEqual(retrived.name, self.user.name)
        self.assertEqual(retrived.email, self.user.email)
        self.assertNotEqual(retrived.updated_at, retrived.created_at)

    def test_delete_method(self):
        """Tests that the delete method removes
        the user instance from the database."""
        self.user.save()
        self.user.delete()
        retrived = db.session.get(User, self.user.id)
        self.assertIsNone(retrived)

    def test_to_dict_method(self):
        """Tests that the to_dict method returns a dict
        with object attributes."""
        expected_dict = {
            "id": self.user.id,
            "created_at": self.user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.user.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            "name": "testuser",
            "email": "testemail@example.com",
        }
        self.assertEqual(self.user.to_dict(), expected_dict)
        self.assertNotIn("_password", self.user.to_dict())

    def test_str_method(self):
        """Tests that the __str__ method returns a
        string representation of the object."""
        dict_rep = self.user.to_dict()
        expected_str = f"[User] ({self.user.id}) {dict_rep}"
        self.assertEqual(self.user.__str__(), expected_str)


if __name__ == "__main__":
    unittest.main()

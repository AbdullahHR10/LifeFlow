"""Module that contains the BaseTestCase."""

import unittest
from backend import create_app, db
from backend.models.user import User


class BaseTestCase(unittest.TestCase):
    """Provides shared setup and teardown methods for all test cases."""
    def setUp(self):
        """Sets up the flask app and database for all tests."""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.user = User(
            name="testuser",
            email="testemail@example.com",
        )

    def tearDown(self):
        """Tears down the Flask app and database after the tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

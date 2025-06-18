"""Module that contains the Note class unittests."""

import unittest
from backend import create_app, db
from backend.models.user import User
from backend.models.note import Note
from backend.utils.enums import BackgroundColor


class TestNoteClass(unittest.TestCase):
    """Unit tests for the Note model."""
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
        self.note = Note(
            id="f47ac10b-58cc-4372-a567-0e02b2c3d479",
            created_at="2025-05-01 22:00:00",
            updated_at="2025-05-02 18:12:00",
            title="Test note",
            content="Test note content",
            background_color=BackgroundColor.BLUE,
            user_id=self.user.id
        )

    def tearDown(self):
        """Tears down the Flask app and database after the tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_id(self):
        """Tests that the note's id is correct."""
        self.assertIsInstance(self.note.id, str)
        self.assertEqual(self.note.id, "f47ac10b-58cc-4372-a567-0e02b2c3d479")

    def test_created_at(self):
        """Tests the note's created_at if it's correct."""
        self.assertIsInstance(self.note.created_at, str)
        self.assertEqual(self.note.created_at, "2025-05-01 22:00:00")

    def test_updated_at(self):
        """Tests the note's updated_at if it's correct."""
        self.assertIsInstance(self.note.updated_at, str)
        self.assertEqual(self.note.updated_at, "2025-05-02 18:12:00")

    def test_title(self):
        """Tests the note's title if it's correct."""
        self.assertIsInstance(self.note.title, str)
        self.assertEqual(self.note.title, "Test note")

    def test_content(self):
        """Tests the note's content if it's correct."""
        self.assertIsInstance(self.note.content, str)
        self.assertEqual(self.note.content, "Test note content")

    def test_background_color(self):
        """Tests the note's category if it's correct."""
        self.assertIsInstance(self.note.background_color, str)
        self.assertEqual(self.note.background_color, "Blue")
        self.assertEqual(self.note.background_color,
                         BackgroundColor.BLUE.value)

    def test_save_method(self):
        """Tests that the save method adds and commits
        the note instance to the database."""
        self.note.background_color = BackgroundColor.BLUE
        self.note.save()
        retrived = db.session.get(Note, self.note.id)
        self.assertIsNotNone(retrived)
        self.assertEqual(retrived.title, self.note.title)
        self.assertEqual(retrived.content, self.note.content)
        self.assertEqual(retrived.background_color, self.note.background_color)

    def test_delete_method(self):
        """Tests that the delete method removes
        the note instance from the database."""
        self.note.background_color = BackgroundColor.BLUE
        self.note.save()
        self.note.delete()
        retrived = db.session.get(Note, self.note.id)
        self.assertIsNone(retrived)

    def test_to_dict_method(self):
        """Tests that the to_dict method returns a dict
        with object attributes."""
        expected_dict = {
            "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "created_at": "2025-05-01 22:00:00",
            "updated_at": "2025-05-02 18:12:00",
            "title": "Test note",
            "content": "Test note content",
            "background_color": BackgroundColor.BLUE.value,
            "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
        }
        self.assertEqual(self.note.to_dict(), expected_dict)

    def test_str_method(self):
        """Tests that the __str__ method returns a
        string representation of the object."""
        dict_rep = self.note.to_dict()
        expected_str = f"[Note] ({self.note.id}) {dict_rep}"
        self.assertEqual(self.note.__str__(), expected_str)


if __name__ == "__main__":
    unittest.main()

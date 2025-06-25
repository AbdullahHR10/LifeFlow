"""Module that contains the database helpers."""

import unittest
from unittest.mock import patch
from backend.tests.base_test import BaseTestCase
from backend.models.note import Note
from backend.utils.enums import BackgroundColor
from backend.utils.db_helpers import get_object, build_object, edit_object
import json


class TestDatabaseHelpers(BaseTestCase):
    """Unit tests for the database helpers."""
    def setUp(self):
        """Extends setup with additional test-specific configurations."""
        super().setUp(login=True, user=True)
        self.note = Note(
            title="Test note",
            content="Test note content",
            background_color=BackgroundColor.BLUE,
            user_id=self.user.id
        )
        self.note.save()

    def test_get_object(self):
        """Tests get_object function."""
        obj = get_object(Note, self.note.id)
        self.assertEqual(obj.id, self.note.id)
        self.assertEqual(obj.title, self.note.title)
        self.assertEqual(obj.content, self.note.content)
        self.assertEqual(obj.background_color, self.note.background_color)
        self.assertEqual(obj.user_id, self.user.id)

    def test_build_object(self):
        """Tests build_object function."""
        payload = {
            "title": "test build_object",
            "content": "test build_object content",
            "background_color": BackgroundColor.BLUE.name
        }
        with self.app.test_request_context(
            method="POST",
            data=json.dumps(payload),
            content_type="application/json"
        ):
            with patch("backend.utils.db_helpers.current_user") as mock_user:
                mock_user.id = self.user.id
                keys = ["title", "content", "background_color"]
                obj = build_object(Note, keys)

                self.assertEqual(obj.title, payload["title"])
                self.assertEqual(obj.content, payload["content"])
                self.assertEqual(obj.background_color,
                                 payload["background_color"])
                self.assertEqual(obj.user_id, self.user.id)

    def test_edit_object(self):
        """Tests edit_object function."""
        payload = {
            "title": "test build_object",
            "content": "test build_object content",
            "background_color": BackgroundColor.BLUE.name
        }
        with self.app.test_request_context(
            method="PATCH",
            data=json.dumps(payload),
            content_type="application/json"
        ):
            with patch("backend.utils.db_helpers.current_user",
                       autospec=True) as mock_user:
                mock_user.id = self.user.id
                keys = ["title", "content", "background_color"]
                updated_obj = edit_object(self.note, keys)

                self.assertEqual(updated_obj.title, payload["title"])
                self.assertEqual(updated_obj.content, payload["content"])
                self.assertEqual(updated_obj.background_color,
                                 payload["background_color"])
                self.assertEqual(updated_obj.user_id, self.user.id)


if __name__ == "__main__":
    unittest.main()

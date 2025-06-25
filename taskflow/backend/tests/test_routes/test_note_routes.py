"""Module that contains unit tests for note routes."""

import unittest
from backend.tests.base_test import BaseTestCase
from backend.models.note import Note
from backend.utils.enums import BackgroundColor


class TestNoteRoutes(BaseTestCase):
    """Unit tests for Note routes."""
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

    def test_get_notes(self):
        """Tests GET /notes route."""
        response = self.client.get("/api/note/notes")
        response_data = response.get_json()
        expected_data = [self.note.to_dict()]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["data"], expected_data)

    def test_post_notes(self):
        """Tests POST /notes route."""
        note_data = {
            "title": "New Note",
            "content": "This is a test note.",
            "background_color": "BLUE"
        }
        response = self.client.post("/api/note/notes", json=note_data)
        response_data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["data"]["title"], note_data["title"])
        self.assertEqual(
            response_data["data"]["content"],
            note_data["content"]
        )
        self.assertEqual(
            response_data["data"]["background_color"],
            note_data["background_color"]
        )

    def test_patch_notes(self):
        """Tests PATCH /notes/<note_id> route."""
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "background_color": "RED"
        }
        response = self.client.patch(
            f"/api/note/notes/{self.note.id}",
            json=updated_data
        )
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_data["data"]["title"],
            updated_data["title"]
        )
        self.assertEqual(
            response_data["data"]["content"],
            updated_data["content"]
        )
        self.assertEqual(
            response_data["data"]["background_color"],
            updated_data["background_color"]
        )

    def test_delete_notes(self):
        """Tests DELETE /notes/<note_id> route."""
        response = self.client.delete(f"/api/note/notes/{self.note.id}")
        self.assertEqual(response.status_code, 200)

        follow_up = self.client.get("/api/note/notes")
        notes = follow_up.get_json()["data"]
        self.assertNotIn(self.note.to_dict(), notes)


class TestNoteRoutesUnauth(BaseTestCase):
    """Tests that unauthenticated users cannot access note routes."""
    def test_get_notes_unauth(self):
        """Tests that GET /notes returns 401 if unauthed."""
        response = self.client.get("/api/note/notes")
        self.assertEqual(response.status_code, 401)

    def test_post_notes_unauth(self):
        """Tests that POST /notes returns 401 if unauthed."""
        note_data = {
            "title": "Hacker Note",
            "content": "unauth access",
            "background_color": "RED"
        }
        response = self.client.post("/api/note/notes", json=note_data)
        self.assertEqual(response.status_code, 401)

    def test_patch_notes_unauthed(self):
        """Tests that PATCH /notes/<note_id> returns 401 if unauthed."""
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "background_color": "RED"
        }
        fake_note_id = "123"
        response = self.client.patch(
            f"/api/note/notes/{fake_note_id}",
            json=updated_data
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_notes_unauthed(self):
        """Tests that DELETE /notes/<note_id> returns 401 if unauthed."""
        fake_note_id = "123"
        response = self.client.delete(f"/api/note/notes/{fake_note_id}")
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()

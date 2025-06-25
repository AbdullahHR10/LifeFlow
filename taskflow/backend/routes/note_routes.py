"""Module that contains Note routes."""

from flask import Blueprint
from flask_login import current_user, login_required
from ..models.note import Note
from ..utils.db_helpers import get_object, build_object, edit_object
from ..utils.response import json_response

note_bp = Blueprint('note_bp', __name__)
note_keys = ["title", "content", "background_color"]


@note_bp.route("/notes")
@login_required
def notes():
    """Returns current user notes (json)."""
    notes = Note.query.filter_by(user_id=current_user.id).order_by(
        Note.updated_at.desc()).all()
    notes_list = [note.to_dict() for note in notes]
    return json_response(
        status="success",
        data=notes_list
    ), 200


@note_bp.route("/notes", methods=["POST"])
@login_required
def create_note():
    """Creates a new note."""
    new_note = build_object(Note, note_keys)
    new_note.save(refresh=True)

    return json_response(
        status="success",
        message="Note created successfully",
        data=new_note.to_dict()
    ), 201


@note_bp.route("/notes/<string:note_id>", methods=["PATCH"])
@login_required
def edit_note(note_id):
    """Edits a note."""
    note = get_object(Note, note_id)
    edit_object(note, note_keys)
    note.save(refresh=True)

    return json_response(
        status="success",
        message="Note updated successfully",
        data=note.to_dict()
    ), 200


@note_bp.route("/notes/<string:note_id>", methods=["DELETE"])
@login_required
def delete_note(note_id):
    """Deletes a note."""
    note = get_object(Note, note_id)
    note.delete()

    return json_response(
        status="success",
        message="Note deleted successfully"
    ), 200

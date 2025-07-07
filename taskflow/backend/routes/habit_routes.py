"""
Module that contains Habit routes.

This module defines all HTTP endpoints for managing habits:
- Listing habits with pagination
- Creating, editing, and deleting habits
- Marking habits as complete to track streaks
- Returning habit data for the authenticated user

All routes require authentication, and most require ownership validation.
"""

from flask import Blueprint, request
from flask_login import current_user, login_required
from backend import limiter
from ..models.habit import Habit
from ..utils.db_helpers import build_object, edit_object
from ..utils.response import json_response
from ..utils.logger import logger
from flasgger import swag_from
from ..utils.doc_path import doc_path
from ..schemas.habit_schema import HabitSchema
from ..decorators.ownership import ownership_required

habit_bp = Blueprint('habit_bp', __name__)
habit_schema = HabitSchema()
HABIT_KEYS = ["title", "description", "frequency", "target_count",
              "priority", "category", "background_color"]


@habit_bp.route("/", methods=["GET"])
@swag_from(doc_path("habit/get_habits.yml"))
@limiter.limit("20 per minute")
@login_required
def get_habits():
    """Gets paginated habits for the current user."""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 8, type=int)

    pagination = Habit.query.filter_by(user_id=current_user.id) \
        .order_by(Habit.updated_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    return json_response(
        status="success",
        data={
            "habits": [habit.to_dict() for habit in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page,
            "per_page": pagination.per_page
        }
    ), 200


@habit_bp.route("/", methods=["POST"])
@swag_from(doc_path("habit/create_habit.yml"))
@limiter.limit("10 per minute")
@login_required
def create_habit():
    """Creates a new habit."""
    new_habit = build_object(Habit, HABIT_KEYS, schema=habit_schema)
    new_habit.save(refresh=True)
    logger.info(f"User {current_user.id} created habit {new_habit.id}")

    return json_response(
        status="success",
        message="Habit created successfully",
        data=new_habit.to_dict()
    ), 201


@habit_bp.route("/<string:habit_id>/complete", methods=["PATCH"])
@swag_from(doc_path("habit/complete_habit.yml"))
@limiter.limit("20 per minute")
@login_required
@ownership_required(Habit)
def complete_habit(habit):
    """Marks habit as completed for the current streak."""
    habit.mark_complete()

    return json_response(
        status="success",
        message="Habit marked as completed",
        data=habit.to_dict()
    ), 200


@habit_bp.route("/<string:habit_id>", methods=["PATCH"])
@swag_from(doc_path("habit/edit_habit.yml"))
@limiter.limit("20 per minute")
@login_required
@ownership_required(Habit)
def edit_habit(habit):
    """Edits a habit's fields."""
    edit_object(habit, HABIT_KEYS)
    habit.save(refresh=True)
    logger.info(f"User {current_user.id} edited habit {habit.id}")

    return json_response(
        status="success",
        message="Habit updated successfully",
        data=habit.to_dict()
    ), 200


@habit_bp.route("/<string:habit_id>", methods=["DELETE"])
@swag_from(doc_path("habit/delete_habit.yml"))
@limiter.limit("20 per minute")
@login_required
@ownership_required(Habit)
def delete_habit(habit):
    """Deletes a habit from the database."""
    habit.delete()
    logger.info(F"User ({current_user.id}) has deleted habit {habit.id}.")

    return json_response(
        status="success",
        message="Habit deleted successfully"
    ), 200

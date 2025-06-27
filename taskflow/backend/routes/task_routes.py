"""
Module that contains Task routes.

This module defines all HTTP endpoints for managing tasks:
- Listing tasks with pagination
- Creating, editing, and deleting tasks
- Marking tasks complete
- Returning summary statistics

All routes require authentication, and most require ownership validation.
"""


from flask import Blueprint, request
from flask_login import current_user, login_required
from backend import limiter
from ..models.task import Task
from ..utils.enums import Priority, Category
from collections import Counter
from ..utils.db_helpers import get_object, build_object, edit_object
from ..utils.response import json_response
from ..utils.logger import logger
from flasgger import swag_from
from ..utils.doc_path import doc_path
from ..schemas.task_schema import TaskSchema
from ..decorators.ownership import ownership_required


task_bp = Blueprint('task_bp', __name__)
task_keys = ["title", "description", "priority", "deadline", "category"]
task_schema = TaskSchema()


@task_bp.route("/", methods=["GET"])
@swag_from(doc_path("task/get_tasks.yml"))
@limiter.limit("20 per minute")
@login_required
def get_tasks():
    """Gets paginated tasks for the current user."""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 8, type=int)

    pagination = Task.query.filter_by(user_id=current_user.id) \
        .order_by(Task.updated_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    return json_response(
        status="success",
        data={
            "tasks": [task.to_dict() for task in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page,
            "per_page": pagination.per_page
        }
    ), 200


@task_bp.route("/analytics", methods=["GET"])
@swag_from(doc_path("task/tasks_data.yml"))
@limiter.limit("20 per minute")
@login_required
def tasks_analytics():
    """Gets current user task analytics data."""
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    num_tasks = len(tasks)
    num_completed = sum(task.completed for task in tasks)
    num_unfinished = num_tasks - num_completed

    priority_counts = Counter(task.priority.name for task in tasks)
    category_counts = Counter(task.category.name for task in tasks)

    priorities = [p.name for p in Priority]
    categories = [c.name for c in Category]

    priority_data = {p: priority_counts.get(p, 0) for p in priorities}
    category_data = {c: category_counts.get(c, 0) for c in categories}

    return json_response(
        status="success",
        data={
            "total": num_tasks,
            "completed": num_completed,
            "unfinished": num_unfinished,
            "priorities": priority_data,
            "categories": category_data
        }
    ), 200


@task_bp.route("/", methods=["POST"])
@swag_from(doc_path("task/create_task.yml"))
@limiter.limit("10 per minute")
@login_required
def create_task():
    """Creates a new task."""
    new_task = build_object(Task, task_keys, schema=task_schema)
    new_task.save(refresh=True)
    logger.info(f"User {current_user.id} created task {new_task.id}")

    return json_response(
        status="success",
        message="Task created successfully",
        data=new_task.to_dict()
    ), 201


@task_bp.route("/<string:task_id>/complete", methods=["PATCH"])
@swag_from(doc_path("task/complete_task.yml"))
@limiter.limit("20 per minute")
@login_required
@ownership_required
def complete_task(task_id):
    """Marks task as completed."""
    task = get_object(Task, task_id)
    task.mark_complete()

    return json_response(
        status="success",
        message="Task completed successfully",
        data=task.to_dict()
    ), 200


@task_bp.route("/<string:task_id>", methods=["PATCH"])
@login_required
def edit_task(task):
    """Edits a task's fields."""
    edit_object(task, task_keys)
    task.save(refresh=True)
    logger.info(f"User {current_user.id} edited task {task.id}")

    return json_response(
        status="success",
        message="Task updated successfully",
        data=task.to_dict()
    ), 200


@task_bp.route("/<string:task_id>", methods=["DELETE"])
@swag_from(doc_path("task/delete_task.yml"))
@limiter.limit("20 per minute")
@login_required
@ownership_required
def delete_task(task):
    """Deletes a task from the database."""
    task.delete()
    logger.info(F"User ({current_user.id}) has deleted task {task.id}.")

    return json_response(
        status="success",
        message="Task deleted successfully"
    ), 200


@task_bp.route("/completed", methods=["DELETE"])
@swag_from(doc_path("task/delete_completed_tasks.yml"))
@limiter.limit("20 per minute")
@login_required
@ownership_required
def delete_completed_tasks():
    """Deletes all completed tasks for the current user."""
    completed_tasks = Task.query.filter_by(
        user_id=current_user.id, completed=True).all()

    if not completed_tasks:
        return json_response(
            status="error",
            message="No completed tasks found"
        ), 404

    for task in completed_tasks:
        task.delete()

    return json_response(
        status="success",
        message="All completed tasks deleted successfully"
    ), 200

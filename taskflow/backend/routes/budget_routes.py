"""Module that contains Budget routes.

This module defines API endpoints for:
- Listing user budgets
- Creating new budgets
- Editing and deleting budgets

All routes require authentication, and most require ownership validation.
"""


from flask import Blueprint, request
from flask_login import current_user, login_required
from backend import limiter
from ..models.budget import Budget
from ..utils.db_helpers import build_object, edit_object
from ..utils.response import json_response
from ..utils.logger import logger
from flasgger import swag_from
from ..utils.doc_path import doc_path
from ..schemas.budget_schema import BudgetSchema
from ..decorators.ownership import ownership_required


budget_bp = Blueprint('budget_bp', __name__)
budget_schema = BudgetSchema()
BUDGET_KEYS = ["category", "amount", "period", "start_date", "end_date"]


@budget_bp.route("/", methods=["GET"])
@swag_from(doc_path("budget/get_budgets.yml"))
@limiter.limit("20 per minute")
@login_required
def get_budgets():
    """Gets paginated budgets for the current user."""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 12, type=int)

    pagination = Budget.query.filter_by(user_id=current_user.id) \
        .order_by(Budget.updated_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    return json_response(
        status="success",
        data={
            "budgets": [budget.to_dict() for budget in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page,
            "per_page": pagination.per_page
        }
    ), 200


@budget_bp.route("/", methods=["POST"])
@swag_from(doc_path("budget/create_budget.yml"))
@limiter.limit("10 per minute")
@login_required
def create_budget():
    """Creates a new budget."""
    new_budget = build_object(Budget, BUDGET_KEYS, schema=budget_schema)
    new_budget.save(refresh=True)
    logger.info(f"User {current_user.id} created budget {new_budget.id}")

    return json_response(
        status="success",
        message="Budget created successfully",
        data=new_budget.to_dict()
    ), 201


@budget_bp.route("/<string:budget_id>", methods=["PATCH"])
@swag_from(doc_path("budget/edit_budget.yml"))
@limiter.limit("10 per minute")
@login_required
@ownership_required(Budget)
def edit_budget(budget):
    """Edits a budget."""
    edit_object(budget, BUDGET_KEYS, schema=budget_schema)
    budget.save(refresh=True)
    logger.info(f"User {current_user.id} edited budget {budget.id}")

    return json_response(
        status="success",
        message="Budget updated successfully",
        data=budget.to_dict()
    ), 200


@budget_bp.route("/<string:budget_id>", methods=["DELETE"])
@swag_from(doc_path("budget/delete_budget.yml"))
@limiter.limit("5 per minute")
@login_required
@ownership_required(Budget)
def delete_budget(budget):
    """Deletes a budget."""
    budget.delete()
    logger.info(f"User {current_user.id} deleted budget {budget.id}")

    return json_response(
        status="success",
        message="Budget deleted successfully"
    ), 200

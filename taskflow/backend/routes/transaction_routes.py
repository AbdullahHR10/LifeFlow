"""Module that contains Transaction routes.

This module defines API endpoints for:
- Listing user transactions
- Creating new transactions
- Editing and deleting transactions

All routes require authentication, and most require ownership validation.
"""

from flask import Blueprint, request
from flask_login import current_user, login_required
from backend import limiter
from ..models.transaction import Transaction
from ..utils.db_helpers import build_object, edit_object, recalculate_budget
from ..utils.response import json_response
from ..utils.logger import logger
from flasgger import swag_from
from ..utils.doc_path import doc_path
from ..schemas.transaction_schema import TransactionSchema
from ..decorators.ownership import ownership_required


transaction_bp = Blueprint('transaction_bp', __name__)
transaction_schema = TransactionSchema()
TRANSACTION_KEYS = ["title", "description", "amount",
                    "type", "date", "category"]


@transaction_bp.route("/", methods=["GET"])
@swag_from(doc_path("transaction/get_transactions.yml"))
@limiter.limit("20 per minute")
@login_required
def get_transactions():
    """Gets paginated transactions for the current user."""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 12, type=int)

    pagination = Transaction.query.filter_by(user_id=current_user.id) \
        .order_by(Transaction.date.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    return json_response(
        status="success",
        data={
            "transactions": [
                transaction.to_dict() for transaction in pagination.items
            ],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page,
            "per_page": pagination.per_page
        }
    ), 200


@transaction_bp.route("/", methods=["POST"])
@swag_from(doc_path("transaction/create_transaction.yml"))
@limiter.limit("10 per minute")
@login_required
def create_transaction():
    """Creates a new transaction."""
    new_transaction = build_object(
        Transaction, TRANSACTION_KEYS, schema=transaction_schema
    )
    new_transaction.save(refresh=True)
    logger.info(f"User {current_user.id} created transaction "
                f"{new_transaction.id}")

    recalculate_budget(
        user_id=current_user.id,
        category=new_transaction.category,
        start_date=new_transaction.date,
        end_date=new_transaction.date
    )

    return json_response(
        status="success",
        message="Transaction created successfully",
        data=new_transaction.to_dict()
    ), 201


@transaction_bp.route("/<string:transaction_id>", methods=["PATCH"])
@swag_from(doc_path("transaction/edit_transaction.yml"))
@limiter.limit("10 per minute")
@login_required
@ownership_required(Transaction)
def edit_transaction(transaction):
    """Edits a transaction."""
    edit_object(transaction, TRANSACTION_KEYS, schema=transaction_schema)
    transaction.save(refresh=True)
    logger.info(f"User {current_user.id} edited transaction {transaction.id}")

    recalculate_budget(
        user_id=current_user.id,
        category=transaction.category,
        start_date=transaction.date,
        end_date=transaction.date
    )

    return json_response(
        status="success",
        message="Transaction updated successfully",
        data=transaction.to_dict()
    ), 200


@transaction_bp.route("/<string:transaction_id>", methods=["DELETE"])
@swag_from(doc_path("transaction/delete_transaction.yml"))
@limiter.limit("5 per minute")
@login_required
@ownership_required(Transaction)
def delete_transaction(transaction):
    """Deletes a transaction."""
    transaction.delete()
    logger.info(f"User {current_user.id} deleted transaction {transaction.id}")

    recalculate_budget(
        user_id=current_user.id,
        category=transaction.category,
        start_date=transaction.date,
        end_date=transaction.date
    )

    return json_response(
        status="success",
        message="Transaction deleted successfully."
    ), 200

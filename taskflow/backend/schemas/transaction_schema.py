"""Module that contains the Transaction schema."""
from marshmallow import Schema, fields, validate
from ..utils.enums import TransactionType, BudgetCategory


class TransactionSchema(Schema):
    """Class that defines the schema of Transaction."""
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1)
    )
    description = fields.Str(
        validate=validate.Length(min=0)
    )
    amount = fields.Float(
        required=True,
        validate=validate.Range(min=0)
    )
    type = fields.Str(
        required=True,
        validate=validate.OneOf([t.name for t in TransactionType])
    )
    date = fields.Date(required=True)
    category = fields.Str(
        required=True,
        validate=validate.OneOf([c.name for c in BudgetCategory])
    )

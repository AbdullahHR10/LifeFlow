"""Module that contains the Budget schema."""
from marshmallow import fields, validate
from ..utils.enums import BudgetCategory, Frequency
from . import BaseSchema


class BudgetSchema(BaseSchema):
    """Class that defines the schema of Budget."""
    category = fields.Str(
        required=True,
        validate=validate.OneOf([c.name for c in BudgetCategory])
    )
    amount = fields.Float(
        required=True,
        validate=validate.Range(min=0)
    )
    spent = fields.Float(
        load_default=0.0,
        validate=validate.Range(min=0)
    )
    period = fields.Str(
        required=True,
        validate=validate.OneOf([p.name for p in Frequency])
    )
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

"""Module that contains the Task schema."""
from marshmallow import fields, validate
from ..utils.enums import Priority, Category
from . import BaseSchema


class TaskSchema(BaseSchema):
    """Class that defines the schema of Task."""
    title = fields.Str(required=True, validate=validate.Length(min=3, max=30))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    priority = fields.Str(
        required=True,
        validate=validate.OneOf([priority.name for priority in Priority])
    )
    deadline = fields.Date(required=True)
    completed = fields.Bool(required=False)
    category = fields.Str(
        required=True,
        validate=validate.OneOf([category.name for category in Category])
    )
    completed_at = fields.DateTime(required=False)

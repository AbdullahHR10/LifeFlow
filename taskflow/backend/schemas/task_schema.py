"""Module that contains the Task schema."""
from marshmallow import Schema, fields, validate
from ..utils.enums import Priority, Category


class TaskSchema(Schema):
    """Class that defines the schema of Task."""
    title = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    priority = fields.Str(
        validate=validate.OneOf([priority.name for priority in Priority])
    )
    deadline = fields.Date(required=True)
    completed = fields.Bool(missing=False)
    category = fields.Str(
        validate=validate.OneOf([category.name for category in Category])
    )
    completed_at = fields.DateTime(required=False)

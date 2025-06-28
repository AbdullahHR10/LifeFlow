"""Module that contains the Note schema."""
from marshmallow import Schema, fields, validate
from ..utils.enums import BackgroundColor


class NoteSchema(Schema):
    """Class that defines the schema of Note."""
    title = fields.Str(required=True, validate=validate.Length(min=1))
    content = fields.Str(required=True, validate=validate.Length(min=1))
    background_color = fields.Str(
        validate=validate.OneOf([color.name for color in BackgroundColor])
    )

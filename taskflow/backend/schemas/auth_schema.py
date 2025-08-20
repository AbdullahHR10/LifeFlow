"""Module that contains the Auth schemas."""
from marshmallow import fields, validate, validates_schema
from backend.utils.validators import send_validation_error
from . import BaseSchema


class SignupSchema(BaseSchema):
    """Class that defines the schema of Signup."""
    name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=30)
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6)
    )
    confirm_password = fields.Str(required=True)

    @validates_schema
    def validate_password_match(self, data, **kwargs):
        """Validation to ensure the passwords match."""
        if data.get("password") != data.get("confirm_password"):
            send_validation_error(
                "confirm_password",
                "Passwords do not match."
            )


class LoginSchema(BaseSchema):
    """Class that defines the schema of Login."""
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    remember = fields.Boolean(load_default=False)

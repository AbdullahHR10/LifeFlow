"""Module that contains database helpers."""
from flask import abort, request
from flask_login import current_user
from backend import db
import bleach


def sanitize_input(data: dict, keys: list[str]) -> dict:
    """
    Sanitizes input fields using bleach.

    Args:
        data (dict): data containing potentially unsafe user data.
        keys (list[str]): The list that will be sanitized.

    Returns:
        Dictionary with the specified keys sanitized.
    """
    sanitized = {}
    for key in keys:
        value = data.get(key)
        if isinstance(value, str):
            sanitized[key] = bleach.clean(value)
        else:
            sanitized[key] = value

    return sanitized


def get_object(model: type, obj_id: str) -> object:
    """
    Retrieves an object by ID and ensures it belongs to the current user.

    Args:
        model (type): The model class to query.
        obj_id (str): The ID of the object to retrieve.

    Returns:
        object: The authorized object instance.
    """
    obj = db.session.get(model, obj_id)

    if not obj or obj.user_id != current_user.id:
        abort(404, "object not found or unauthorized")

    return obj


def build_object(model: type, keys: list[str], schema=None) -> object:
    """
    Builds an instance of the given model using JSON data from the request.

    Args:
        model (type): The model class to instantiate.
        keys (list[str]): List of keys to extract from the JSON payload.
        user_id (str): The user ID to include in the created object.

    Returns:
        An instance of `model` with the extracted data and user id.
    """
    data = request.get_json()

    if schema:
        from marshmallow import ValidationError
        try:
            obj_data = schema.load(data)
        except ValidationError as e:
            abort(404, description={
                "status": "error",
                "message": "Validation failed",
                "data": e.messages
            }), 400
    else:
        obj_data = {key: data.get(key) for key in keys}

    obj_data = sanitize_input(obj_data, keys)
    obj_data["user_id"] = current_user.id
    return model(**obj_data)


def edit_object(obj: object, keys: list[str], schema=None) -> object:
    """
    Updates the provided object's attributes using JSON data from the request.

    Args:
        obj (object): The SQLAlchemy model instance to be edited.
        keys (list[str]): List of keys to extract from the JSON payload.

    Returns:
        object: The updated object instance with modified fields.
    """
    data = request.get_json()

    if schema:
        from marshmallow import ValidationError
        try:
            schema.load(data, partial=True)
        except ValidationError as e:
            abort(400, {"status": "error",
                        "message": "Validation failed", "data": e.messages})

    data = sanitize_input(data, keys)
    for key in keys:
        if key in data:
            setattr(obj, key, data[key])
    return obj

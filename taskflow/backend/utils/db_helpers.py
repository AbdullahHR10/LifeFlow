"""Module that contains database helpers."""

from flask import abort, request
from flask_login import current_user
from backend import db


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
        abort(404)

    return obj


def build_object(model: type, keys: list[str]) -> object:
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
    obj_data = {key: data.get(key) for key in keys}
    obj_data["user_id"] = current_user.id
    return model(**obj_data)


def edit_object(obj: object, keys: list[str]) -> object:
    """
    Updates the provided object's attributes using JSON data from the request.

    Args:
        obj (object): The SQLAlchemy model instance to be edited.
        keys (list[str]): List of keys to extract from the JSON payload.

    Returns:
        object: The updated object instance with modified fields.
    """
    data = request.get_json()
    for key in keys:
        if key in data:
            setattr(obj, key, data[key])
    return obj

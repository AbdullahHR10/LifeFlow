"""Module that contains database helpers."""

from flask import request
from flask_login import current_user


def build_object(model: type, keys: list[str]):
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

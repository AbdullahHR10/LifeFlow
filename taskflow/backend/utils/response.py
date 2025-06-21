"""Module that contains response utils."""
from typing import Any, Optional
from flask import jsonify, Response


def json_response(
    status: str,
    data: Optional[Any] = None,
    message: str = "",
) -> Response:
    """
    Generates a standardized JSON HTTP response for Flask routes.

    Args:
        status (str): Status of the response, defaults to 'success'
        data (Any, optional): The data payload to include in the response.
        message (str): A message for info or errors to explain the response.

    Returns:
        Response: A Flask `Response` object with the JSON response body.
    """
    response = {
        "status": status,
        "data": data,
        "message": message
    }
    return jsonify(response)

"""Module that contains response utils tests."""
import pytest
from backend.utils.response import json_response


def test_valid_json_response(app):
    """Tests valid json_response."""
    status = "success"
    data = {"key": "value"}
    message = "data sent successfully"
    response = json_response(status, data, message)
    assert response.status_code == 200
    assert response.get_json() == json_response(
        status, data, message).get_json()


def test_without_status_json_reponse(app):
    """Tests without status json_response."""
    data = {"key": "value"}
    message = "data sent successfully"
    with pytest.raises(TypeError):
        json_response(data=data, message=message)


def test_without_data_and_message_json_reponse(app):
    """Tests without status json_response."""
    response = json_response(status="success", data=None, message=None)
    assert response.get_json() == {
        "status": "success",
        "data": None,
        "message": None
    }

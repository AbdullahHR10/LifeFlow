"""
Module that contains Auth routes.

This module defines API endpoints for:
- Signing up new users
- Logging users in and out
- Generating CSRF tokens

Includes CSRF protection, rate limiting, input validation, and Swagger docs.
"""


from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flasgger import swag_from
from backend import limiter
from flask_wtf.csrf import generate_csrf
from backend.utils.response import json_response
from backend.utils.logger import logger
from backend.utils.doc_path import doc_path
from ..models.user import User
from ..schemas.auth_schema import SignupSchema, LoginSchema


auth_bp = Blueprint("auth_bp", __name__)
signup_schema = SignupSchema()
login_schema = LoginSchema()


@auth_bp.route("/csrf-token", methods=["GET"])
def get_csrf_token():
    """Gets csrf token."""
    token = generate_csrf()
    response = jsonify({"csrf_token": token})
    response.set_cookie("csrf_token", token, samesite="Strict", secure=True)
    return response


@auth_bp.route('/signup', methods=["POST"])
@swag_from(doc_path("auth/signup.yml"))
@limiter.limit("5 per minute")
def signup():
    """Signs a new user up and saves the user to the database."""
    data = request.get_json()
    validated_data = signup_schema.load(data)

    email = validated_data["email"]
    name = validated_data["name"]
    password = validated_data["password"]

    if User.query.filter_by(email=email).first():
        return json_response(
            status="error",
            message="This email is associated with another account"
        ), 400

    new_user = User(
        name=name,
        email=email,
        password=password
    )
    new_user.save()

    login_user(new_user, remember=True)
    logger.info(f"New user has signed up: "
                f"{name} {email} IP: {request.remote_addr}")

    return json_response(
        status="success",
        message="User signed up successfully!"
    ), 201


@auth_bp.route("/login", methods=["POST"])
@swag_from(doc_path("auth/login.yml"))
@limiter.limit("10 per minute")
def login():
    """Logs the user in."""
    data = request.get_json()
    validated_data = login_schema.load(data)

    email = validated_data["email"].strip().lower()
    password = validated_data["password"]
    remember = validated_data.get("remember", False)

    user = User.query.filter_by(email=email).first()
    if not user:
        return json_response(
            status="error",
            message="Invalid credentials"
        ), 401

    if not user.check_password(password):
        return json_response(
            status="error",
            message="Invalid credentials"
        ), 401

    login_user(user, remember=remember)
    logger.info(f"User logged in: {email} IP: {request.remote_addr}")

    return json_response(
        status="success",
        message="User logged in successfully!"
    ), 200


@auth_bp.route("/logout", methods=["POST"])
@swag_from(doc_path("auth/logout.yml"))
@limiter.limit("20 per minute")
@login_required
def logout():
    """Logs the user out."""
    logger.info(f"User logged out: {current_user.email}")
    logout_user()

    return json_response(
        status="success",
        message="User logged out successfully."
    ), 200


from flask import Blueprint, request, jsonify
from .extensions import db
from .models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Check required fields
    if not username or not email or not password:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "username, email, and password are required"
        }), 400

    # Check duplicate username
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({
            "code": "USER_ALREADY_EXISTS",
            "message": "Username already exists"
        }), 409

    # Check duplicate email
    existing_email = User.query.filter_by(email=email).first()

    if existing_email:
        return jsonify({
            "code": "USER_ALREADY_EXISTS",
            "message": "Email already exists"
        }), 409

    # Create user and hash password
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    # Save to database
    db.session.add(new_user)
    db.session.commit()

    # Return successful registration
    return jsonify({
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }), 201


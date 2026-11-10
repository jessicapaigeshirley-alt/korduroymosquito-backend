import jwt
from functools import wraps
from flask import g
from datetime import datetime, timedelta, timezone
from flask import current_app
from flask import Blueprint, request, jsonify
from .extensions import db
from .models import User

auth_bp = Blueprint("auth", __name__)
def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({
                "code": "UNAUTHORIZED",
                "message": "Missing or invalid authorization token"
            }), 401

        token = parts[1]

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET"],
                algorithms=["HS256"]
            )
            g.user_id = int(payload["sub"])

        except jwt.ExpiredSignatureError:
            return jsonify({
                "code": "UNAUTHORIZED",
                "message": "Token has expired"
            }), 401

        except (jwt.PyJWTError, KeyError, ValueError, TypeError):
            return jsonify({
                "code": "UNAUTHORIZED",
                "message": "Missing or invalid authorization token"
            }), 401

        return f(*args, **kwargs)

    return decorated_function

def admin_required(f):
    @wraps(f)
    @auth_required
    def decorated_function(*args, **kwargs):
        user = db.session.get(User, g.user_id)

        if user is None or user.role != "admin":
            return jsonify({
                "code": "FORBIDDEN",
                "message": "Admin access required"
            }), 403

        return f(*args, **kwargs)

    return decorated_function

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

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    # Use the same response for invalid credentials
    invalid_credentials = {
        "code": "INVALID_CREDENTIALS",
        "message": "Invalid username or password"
    }

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify(invalid_credentials), 401

    # Look up the user
    user = User.query.filter_by(username=username).first()

    # Reject incorrect username or password
    if user is None or not user.check_password(password):
        return jsonify(invalid_credentials), 401

    # Create token expiration in UTC
    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=current_app.config["JWT_EXPIRATION_MINUTES"]
    )

    # Create signed JWT
    token = jwt.encode(
        {
            "sub": str(user.id),
            "role": user.role,
            "exp": expiration
        },
        current_app.config["JWT_SECRET"],
        algorithm="HS256"
    )

    return jsonify({
        "access_token": token,
        "token_type": "Bearer"
    }), 200

@auth_bp.get("/me")
@auth_required
def get_my_profile():
    user = User.query.get(g.user_id)

    if user is None:
        return jsonify({
            "code": "USER_NOT_FOUND",
            "message": "User not found"
        }), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }), 200

@auth_bp.patch("/me")
@auth_required
def update_my_profile():
    user = db.session.get(User, g.user_id)

    if user is None:
        return jsonify({
            "code": "USER_NOT_FOUND",
            "message": "User not found"
        }), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "A JSON object is required"
        }), 400

    allowed_fields = {"username", "email"}

    if not any(field in data for field in allowed_fields):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Provide username or email to update"
        }), 400

    if any(field not in allowed_fields for field in data):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Only username and email can be updated"
        }), 400

    for field in allowed_fields:
        if field in data:
            value = data[field]

            if not isinstance(value, str) or not value.strip():
                return jsonify({
                    "code": "VALIDATION_ERROR",
                    "message": f"{field} must be a non-empty string"
                }), 400

            setattr(user, field, value.strip())

    db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }), 200

@auth_bp.get("/admin/ping")
@admin_required
def admin_ping():
    return jsonify({
        "status": "ok",
        "role": "admin"
    }), 200

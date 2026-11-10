from .auth import auth_required
from flask import Blueprint, jsonify

listings_bp = Blueprint("listings", __name__)


@listings_bp.get("/api/korduroymosquito/listings")
@auth_required
def get_listings():
    return jsonify({"listings": []}), 200


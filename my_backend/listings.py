
from flask import Blueprint, jsonify

listings_bp = Blueprint("listings", __name__)


@listings_bp.get("/api/korduroymosquito/listings")
def get_listings():
    return jsonify({"listings": []}), 200


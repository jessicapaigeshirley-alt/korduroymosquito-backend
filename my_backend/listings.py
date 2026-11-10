from decimal import Decimal, InvalidOperation
from flask import Blueprint, jsonify, request, g

from .auth import auth_required
from .extensions import db
from .models import Listing

listings_bp = Blueprint("listings", __name__)



@listings_bp.get("/api/korduroymosquito/listings")
@auth_required
def list_listings():
    page_raw = request.args.get("page", "1")
    per_page_raw = request.args.get("per_page", "10")

    try:
        page = int(page_raw)
        per_page = int(per_page_raw)
    except (ValueError, TypeError):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "page and per_page must be valid integers"
        }), 400

    if page < 1 or per_page < 1 or per_page > 50:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "page must be at least 1 and per_page must be between 1 and 50"
        }), 400

    query = Listing.query.filter_by(
        user_id=g.user_id
    ).order_by(Listing.id.asc())

    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "listings": [
            {
                "id": listing.id,
                "user_id": listing.user_id,
                "title": listing.title,
                "description": listing.description,
                "price": str(listing.price),
                "category": listing.category,
                "condition": listing.condition
            }
            for listing in pagination.items
        ],
        "page": page,
        "per_page": per_page,
        "total": pagination.total,
        "pages": pagination.pages
    }), 200

@listings_bp.get("/api/korduroymosquito/listings/<int:listing_id>")
@auth_required
def get_listing(listing_id):
    listing = db.session.get(Listing, listing_id)

    if listing is None:
        return jsonify({
            "code": "NOT_FOUND",
            "message": "Listing not found"
        }), 404

    if listing.user_id != g.user_id:
        return jsonify({
            "code": "FORBIDDEN",
            "message": "You do not own this listing"
        }), 403

    return jsonify({
        "id": listing.id,
        "user_id": listing.user_id,
        "title": listing.title,
        "description": listing.description,
        "price": str(listing.price),
        "category": listing.category,
        "condition": listing.condition
    }), 200

@listings_bp.post("/api/korduroymosquito/listings")
@auth_required
def create_listing():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "code": "INVALID_REQUEST",
            "message": "A JSON object is required"
        }), 400

    title = data.get("title")
    price = data.get("price")

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Title is required"
        }), 400

    if len(title.strip()) > 150:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Title must be 150 characters or fewer"
        }), 400

    try:
        if isinstance(price, bool) or price is None:
            raise ValueError()
        amount = Decimal(str(price))
        if not amount.is_finite() or amount < 0 or amount.as_tuple().exponent < -2 or amount >= Decimal("100000000"):
            raise ValueError()
    except (InvalidOperation, ValueError):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Price must be a valid nonnegative amount with at most two decimal places"
        }), 400

    listing = Listing(
        title=title.strip(),
        price=amount,
        description=data.get("description"),
        category=data.get("category"),
        condition=data.get("condition"),
        user_id=g.user_id
    )

    db.session.add(listing)
    db.session.commit()

    return jsonify({
        "id": listing.id,
        "user_id": listing.user_id,
        "title": listing.title,
        "description": listing.description,
        "price": str(listing.price),
        "category": listing.category,
        "condition": listing.condition
    }), 201

@listings_bp.patch("/api/korduroymosquito/listings/<int:listing_id>")
@auth_required
def update_listing(listing_id):
    listing = db.session.get(Listing, listing_id)
    if listing is None:
        return jsonify({
            "code": "NOT_FOUND",
            "message": "Listing not found"
        }), 404

    if listing.user_id != g.user_id:
        return jsonify({
            "code": "FORBIDDEN",
            "message": "You do not own this listing"
        }), 403

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "code": "INVALID_REQUEST",
            "message": "A JSON object is required"
        }), 400

    allowed_fields = {
        "title", "description", "price", "category", "condition"
    }

    if not data or any(field not in allowed_fields for field in data):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Provide at least one valid editable field"
        }), 400

    if "title" in data:
        title = data["title"]
        if not isinstance(title, str) or not title.strip() or len(title.strip()) > 150:
            return jsonify({
                "code": "VALIDATION_ERROR",
                "message": "Title must be 1 to 150 characters"
            }), 400
        listing.title = title.strip()

    if "price" in data:
        try:
            price = data["price"]
            if isinstance(price, bool) or price is None:
                raise ValueError()
            amount = Decimal(str(price))
            if (not amount.is_finite() or amount < 0
                    or amount.as_tuple().exponent < -2
                    or amount >= Decimal("100000000")):
                raise ValueError()
        except (InvalidOperation, ValueError):
            return jsonify({
                "code": "VALIDATION_ERROR",
                "message": "Price must be a valid nonnegative amount with at most two decimal places"
            }), 400
        listing.price = amount

    for field in ("description", "category", "condition"):
        if field in data:
            value = data[field]
            if value is not None and not isinstance(value, str):
                return jsonify({
                    "code": "VALIDATION_ERROR",
                    "message": f"{field} must be a string or null"
                }), 400
            setattr(listing, field, value)

    db.session.commit()

    return jsonify({
        "id": listing.id,
        "user_id": listing.user_id,
        "title": listing.title,
        "description": listing.description,
        "price": str(listing.price),
        "category": listing.category,
        "condition": listing.condition
    }), 200

@listings_bp.delete("/api/korduroymosquito/listings/<int:listing_id>")
@auth_required
def delete_listing(listing_id):
    listing = db.session.get(Listing, listing_id)

    if listing is None:
        return jsonify({
            "code": "NOT_FOUND",
            "message": "Listing not found"
        }), 404

    if listing.user_id != g.user_id:
        return jsonify({
            "code": "FORBIDDEN",
            "message": "You do not own this listing"
        }), 403

    db.session.delete(listing)
    db.session.commit()

    return "", 204

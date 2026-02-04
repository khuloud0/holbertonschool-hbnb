#!/usr/bin/python3
"""Amenities API"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace(
    "amenities",
    description="Amenities operations",
    security="Bearer"
)

# ========================
# Models
# ========================

amenity_model = api.model(
    "Amenity",
    {
        "id": fields.String(readonly=True),
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "created_at": fields.DateTime(readonly=True),
        "updated_at": fields.DateTime(readonly=True),
    },
)

# ========================
# /amenities
# ========================

@api.route("/")
class AmenityList(Resource):

    @api.marshal_list_with(amenity_model)
    def get(self):
        """Retrieve all amenities (public)"""
        return facade.get_all_amenities()

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def post(self):
        """Create a new amenity (ADMIN ONLY)"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)

        if not current_user or not current_user.is_admin:
            return {"error": "Admin privileges required"}, 403

        return facade.create_amenity(api.payload)


# ========================
# /amenities/<amenity_id>
# ========================

@api.route("/<amenity_id>")
class AmenityResource(Resource):

    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Retrieve amenity by ID (public)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model)
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def put(self, amenity_id):
        """Update amenity (ADMIN ONLY)"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)

        if not current_user or not current_user.is_admin:
            return {"error": "Admin privileges required"}, 403

        amenity = facade.update_amenity(amenity_id, api.payload)
        if not amenity:
            api.abort(404, "Amenity not found")

        return amenity

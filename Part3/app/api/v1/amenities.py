#!/usr/bin/python3
"""Amenities API"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.services.facade import facade

# ✅ الإضافة هنا فقط
api = Namespace(
    "amenities",
    description="Amenities operations",
    security="Bearer"
)

amenity_model = api.model(
    "Amenity",
    {
        "id": fields.String(readonly=True),
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime,
    },
)


@api.route("/")
class AmenityList(Resource):

    @api.marshal_list_with(amenity_model)
    def get(self):
        """Retrieve all amenities (public)"""
        return facade.get_all_amenities()

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    @jwt_required()  # 🔐 جاهز للحماية (حتى لو ما استخدمنا admin الآن)
    def post(self):
        """Create a new amenity (authenticated users)"""
        return facade.create_amenity(api.payload)


@api.route("/<amenity_id>")
class AmenityResource(Resource):

    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Retrieve amenity by ID (public)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity

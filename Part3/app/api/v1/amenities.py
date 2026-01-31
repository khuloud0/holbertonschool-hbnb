#!/usr/bin/python3
"""Amenities API"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("amenities", description="Amenities operations")

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
        return facade.get_all_amenities()

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        return facade.create_amenity(api.payload)


@api.route("/<amenity_id>")
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity

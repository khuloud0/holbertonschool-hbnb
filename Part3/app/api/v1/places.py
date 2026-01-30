#!/usr/bin/python3
"""Places API endpoints"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('places', description='Place operations')

# ===== Swagger Models =====

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(),
    'description': fields.String(),
    'price': fields.Float(),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
})

# ===== Routes =====

@api.route('/')
class PlaceList(Resource):

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place created successfully')
    @api.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        """Create a new place (authenticated users only)"""
        data = api.payload

        # owner هو المستخدم الحالي
        data['owner_id'] = get_jwt_identity()

        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve all places (public)"""
        places = facade.get_all_places()
        return {'places': [p.to_dict() for p in places]}, 200


@api.route('/<place_id>')
class PlaceResource(Resource):

    def get(self, place_id):
        """Retrieve a place by ID (public)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        """Update a place (owner or admin)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)

        # ✅ admin bypass
        if not current_user.is_admin and place.owner_id != current_user_id:
            return {'error': 'You can only modify your own places'}, 403

        try:
            updated_place = facade.update_place(place_id, api.payload)
            return updated_place.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

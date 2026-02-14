#!/usr/bin/python3
"""Places API endpoints"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace(
    'places',
    description='Place operations',
    security='Bearer'
)

# =========================
# Swagger Models
# =========================

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
})

# =========================
# Routes
# =========================

@api.route('/')
class PlaceList(Resource):

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place created successfully')
    @api.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        """Create a new place (Authenticated users only)"""
        data = api.payload

        # Owner = current logged-in user
        data['owner_id'] = get_jwt_identity()

        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        """Get all places (Public)"""
        places = facade.get_all_places()

        # 🔥 مهم جداً — نرجع List مباشرة
        return [place.to_dict() for place in places], 200


@api.route('/<string:place_id>')
class PlaceResource(Resource):

    def get(self, place_id):
        """Get place by ID (Public)"""
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
        """Update place (Owner or Admin only)"""

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)

        # Admin bypass
        if not current_user.is_admin and place.owner_id != current_user_id:
            return {'error': 'You can only modify your own places'}, 403

        try:
            updated_place = facade.update_place(place_id, api.payload)
            return updated_place.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

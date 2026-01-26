#!/usr/bin/python3
"""Places API endpoints"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('places', description='Place operations')

# ===== Swagger Models =====

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
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
    def post(self):
        place = facade.create_place(api.payload)
        return place.to_dict(), 201

    def get(self):
        places = facade.get_all_places()
        return {'places': [p.to_dict() for p in places]}, 200


@api.route('/<place_id>')
class PlaceResource(Resource):

    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @api.expect(place_update_model, validate=True)
    def put(self, place_id):
        place = facade.update_place(place_id, api.payload)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

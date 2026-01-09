#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

# ========================
# Models
# ========================

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='Owner ID'),
    'amenities': fields.List(
        fields.String,
        description='List of amenity IDs'
    )
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'owner_id': fields.String(description='Owner ID'),
    'amenities': fields.List(
        fields.String,
        description='List of amenity IDs'
    )
})

# ========================
# /places
# ========================

@api.route('/')
class PlaceList(Resource):

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        data = api.payload

        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return {
            'places': [place.to_dict() for place in places]
        }, 200


# ========================
# /places/<place_id>
# ========================

@api.route('/<place_id>')
class PlaceResource(Resource):

    @api.response(200, 'Place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve place by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update place information"""
        data = api.payload

        place = facade.update_place(place_id, data)
        if not place:
            return {'error': 'Place not found'}, 404

        return place.to_dict(), 200

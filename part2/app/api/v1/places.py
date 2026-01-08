#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(
        fields.String,
        required=True,
        description="List of amenities ID's"
    )
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner'),
    'amenities': fields.List(
        fields.String,
        description="List of amenities ID's"
    )
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        if not place_data:
            return {'error': 'Invalid input data'}, 400

        try:
            new_place = facade.create_place(place_data)
            if hasattr(new_place, "id"):
                return {
                    'id': new_place.id,
                    'title': new_place.title,
                    'description': new_place.description,
                    'price': new_place.price,
                    'latitude': new_place.latitude,
                    'longitude': new_place.longitude,
                    'owner_id': new_place.owner_id
                }, 201

            return new_place, 201
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()

        if places and hasattr(places[0], "id"):
            return [
                {
                    'id': p.id,
                    'title': p.title,
                    'latitude': p.latitude,
                    'longitude': p.longitude
                } for p in places
            ], 200

        return places, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id,
            'amenities': getattr(place, 'amenities', [])
        }, 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        if not place_data:
            return {'error': 'Invalid input data'}, 400

        try:
            updated_place = facade.update_place(place_id, place_data)
            if not updated_place:
                return {'error': 'Place not found'}, 404

            if hasattr(updated_place, "id"):
                return {
                    'id': updated_place.id,
                    'title': updated_place.title,
                    'description': updated_place.description,
                    'price': updated_place.price,
                    'latitude': updated_place.latitude,
                    'longitude': updated_place.longitude,
                    'owner_id': updated_place.owner_id,
                    'amenities': getattr(updated_place, 'amenities', [])
                }, 200

            return {'message': 'Place updated successfully'}, 200
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400


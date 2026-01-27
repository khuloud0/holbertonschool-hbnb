from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.place import Place
from app.models.user import User
from app.utils.decorators import admin_required, ownership_required
from app import db

places_bp = Blueprint('places', __name__)

# PUBLIC ENDPOINTS
@places_bp.route('/places', methods=['GET'])
def get_all_places():
    places = Place.query.all()
    return jsonify([place.to_dict() for place in places]), 200

@places_bp.route('/places/<int:place_id>', methods=['GET'])
def get_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    return jsonify(place.to_dict()), 200

# AUTHENTICATED ENDPOINTS
@places_bp.route('/places', methods=['POST'])
@jwt_required()
def create_place():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['name', 'address', 'city', 'country', 'price_per_night', 'max_guests']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        new_place = Place(
            name=data['name'],
            description=data.get('description', ''),
            address=data['address'],
            city=data['city'],
            state=data.get('state', ''),
            country=data['country'],
            price_per_night=float(data['price_per_night']),
            max_guests=int(data['max_guests']),
            latitude=float(data.get('latitude', 0)),
            longitude=float(data.get('longitude', 0)),
            user_id=current_user_id
        )
        
        db.session.add(new_place)
        db.session.commit()
        
        return jsonify(new_place.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@places_bp.route('/places/<int:place_id>', methods=['PUT'])
@jwt_required()
@ownership_required(Place)
def update_place(place_id):
    place = Place.query.get(place_id)
    data = request.get_json()
    
    allowed_fields = ['name', 'description', 'address', 'city', 'state', 
                     'country', 'price_per_night', 'max_guests', 'latitude', 'longitude']
    
    for field in allowed_fields:
        if field in data:
            setattr(place, field, data[field])
    
    try:
        db.session.commit()
        return jsonify(place.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@places_bp.route('/places/<int:place_id>', methods=['DELETE'])
@jwt_required()
@ownership_required(Place)
def delete_place(place_id):
    place = Place.query.get(place_id)
    
    try:
        db.session.delete(place)
        db.session.commit()
        return jsonify({'message': 'Place deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

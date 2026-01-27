from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.amenity import Amenity
from app.utils.decorators import admin_required
from app import db

amenities_bp = Blueprint('amenities', __name__)

# PUBLIC ENDPOINTS
@amenities_bp.route('/amenities', methods=['GET'])
def get_all_amenities():
    amenities = Amenity.query.all()
    return jsonify([amenity.to_dict() for amenity in amenities]), 200

# ADMIN ENDPOINTS
@amenities_bp.route('/amenities', methods=['POST'])
@jwt_required()
@admin_required
def create_amenity():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    existing_amenity = Amenity.query.filter_by(name=data['name']).first()
    if existing_amenity:
        return jsonify({'error': 'Amenity with this name already exists'}), 400
    
    try:
        new_amenity = Amenity(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(new_amenity)
        db.session.commit()
        
        return jsonify(new_amenity.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@amenities_bp.route('/amenities/<int:amenity_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_amenity(amenity_id):
    amenity = Amenity.query.get(amenity_id)
    
    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        if data['name'] != amenity.name:
            existing = Amenity.query.filter_by(name=data['name']).first()
            if existing:
                return jsonify({'error': 'Amenity with this name already exists'}), 400
        amenity.name = data['name']
    
    if 'description' in data:
        amenity.description = data['description']
    
    try:
        db.session.commit()
        return jsonify(amenity.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@amenities_bp.route('/amenities/<int:amenity_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_amenity(amenity_id):
    amenity = Amenity.query.get(amenity_id)
    
    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404
    
    try:
        db.session.delete(amenity)
        db.session.commit()
        return jsonify({'message': 'Amenity deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

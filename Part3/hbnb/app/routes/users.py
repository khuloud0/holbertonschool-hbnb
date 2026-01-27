from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash
from app.models.user import User
from app.utils.decorators import admin_required, ownership_required
from app import db

users_bp = Blueprint('users', __name__)

# PUBLIC ENDPOINTS
@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

# ADMIN ENDPOINTS
@users_bp.route('/users', methods=['POST'])
@jwt_required()
@admin_required
def create_user():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'Email already exists'}), 400
    
    try:
        new_user = User(
            email=data['email'],
            password=data['password'],
            is_admin=data.get('is_admin', False)
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# AUTHENTICATED ENDPOINTS
@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    target_user = User.query.get(user_id)
    
    if not target_user:
        return jsonify({'error': 'User not found'}), 404
    
    if current_user_id != user_id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    if 'email' in data and current_user_id != user_id and not current_user.is_admin:
        return jsonify({'error': 'You cannot change email for other users'}), 400
    
    if 'email' in data and current_user.is_admin:
        if data['email'] != target_user.email:
            existing = User.query.filter_by(email=data['email']).first()
            if existing:
                return jsonify({'error': 'Email already exists'}), 400
        target_user.email = data['email']
    
    if 'password' in data and (current_user_id == user_id or current_user.is_admin):
        target_user.password = generate_password_hash(data['password']).decode('utf-8')
    
    if 'is_admin' in data and current_user.is_admin:
        target_user.is_admin = data['is_admin']
    
    try:
        db.session.commit()
        return jsonify(target_user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

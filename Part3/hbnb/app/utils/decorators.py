from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

def admin_required(f):
    """Ensure user is an admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def ownership_required(model, param_name='id'):
    """Ensure user owns the resource (with admin override)"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            # Get ID from kwargs
            resource_id = kwargs.get(param_name)
            
            # Get resource
            if model == Place:
                resource = Place.query.get(resource_id)
                owner_id = resource.user_id if resource else None
            elif model == Review:
                resource = Review.query.get(resource_id)
                owner_id = resource.user_id if resource else None
            elif model == User:
                resource = User.query.get(resource_id)
                owner_id = resource.id if resource else None
            else:
                return jsonify({'error': 'Invalid model'}), 500
            
            if not resource:
                return jsonify({'error': 'Resource not found'}), 404
            
            # Admin can bypass ownership
            if user.is_admin:
                return f(*args, **kwargs)
            
            # Regular user must be the owner
            if current_user_id != owner_id:
                return jsonify({'error': 'You are not the owner of this resource'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.review import Review
from app.models.place import Place
from app.models.user import User
from app.utils.decorators import admin_required, ownership_required
from app import db

reviews_bp = Blueprint('reviews', __name__)

# PUBLIC ENDPOINTS
@reviews_bp.route('/places/<int:place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    place = Place.query.get(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    
    reviews = Review.query.filter_by(place_id=place_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200

# AUTHENTICATED ENDPOINTS
@reviews_bp.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'text' not in data or 'rating' not in data or 'place_id' not in data:
        return jsonify({'error': 'text, rating, and place_id are required'}), 400
    
    place_id = data['place_id']
    place = Place.query.get(place_id)
    
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    
    if place.user_id == current_user_id:
        return jsonify({'error': 'You cannot review your own place'}), 400
    
    existing_review = Review.query.filter_by(
        user_id=current_user_id, 
        place_id=place_id
    ).first()
    
    if existing_review:
        return jsonify({'error': 'You have already reviewed this place'}), 400
    
    rating = int(data['rating'])
    if rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    try:
        new_review = Review(
            text=data['text'],
            rating=rating,
            user_id=current_user_id,
            place_id=place_id
        )
        
        db.session.add(new_review)
        db.session.commit()
        
        return jsonify(new_review.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@reviews_bp.route('/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
@ownership_required(Review)
def update_review(review_id):
    review = Review.query.get(review_id)
    data = request.get_json()
    
    if 'text' in data:
        review.text = data['text']
    
    if 'rating' in data:
        rating = int(data['rating'])
        if rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        review.rating = rating
    
    try:
        db.session.commit()
        return jsonify(review.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

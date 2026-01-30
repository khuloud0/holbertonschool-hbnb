#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('reviews', description='Review operations')

# =====================
# Models
# =====================

review_model = api.model('Review', {
    'place_id': fields.String(required=True, description='ID of the place'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'text': fields.String(required=True, description='Review text')
})

review_update_model = api.model('ReviewUpdate', {
    'rating': fields.Integer(description='Rating (1-5)'),
    'text': fields.String(description='Review text')
})

# =====================
# /reviews
# =====================

@api.route('/')
class ReviewList(Resource):

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        """Create a new review (authenticated users only)"""
        data = api.payload
        current_user_id = get_jwt_identity()

        place = facade.get_place(data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404

       
        if place.owner_id == current_user_id:
            return {'error': 'You cannot review your own place'}, 403

       
        existing = facade.get_reviews_by_place(data['place_id'])
        for review in existing:
            if review.user_id == current_user_id:
                return {'error': 'You have already reviewed this place'}, 400

        data['user_id'] = current_user_id

        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve all reviews (public)"""
        reviews = facade.get_all_reviews()
        return {'reviews': [review.to_dict() for review in reviews]}, 200


# =====================
# /reviews/<review_id>
# =====================

@api.route('/<review_id>')
class ReviewResource(Resource):

    def get(self, review_id):
        """Retrieve a review by ID (public)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Review not found')
    @jwt_required()
    def put(self, review_id):
        """Update a review (owner only)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        current_user_id = get_jwt_identity()

        if review.user_id != current_user_id:
            return {'error': 'You can only update your own reviews'}, 403

        try:
            updated = facade.update_review(review_id, api.payload)
            return updated.to_dict(), 200
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (owner only)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        current_user_id = get_jwt_identity()

        if review.user_id != current_user_id:
            return {'error': 'You can only delete your own reviews'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


# =====================
# /places/<place_id>/reviews
# =====================

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):

    def get(self, place_id):
        """Retrieve all reviews for a specific place (public)"""
        reviews = facade.get_reviews_by_place(place_id)

        if reviews is None:
            return {'error': 'Place not found'}, 404

        return {'reviews': [review.to_dict() for review in reviews]}, 200

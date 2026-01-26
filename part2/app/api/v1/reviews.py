#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

# =====================
# Models
# =====================

review_model = api.model('Review', {
    'place_id': fields.String(required=True, description='ID of the place'),
    'user_id': fields.String(required=True, description='ID of the user'),
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
    def post(self):
        """Create a new review"""
        data = api.payload
        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return {'reviews': [review.to_dict() for review in reviews]}, 200


# =====================
# /reviews/<review_id>
# =====================

@api.route('/<review_id>')
class ReviewResource(Resource):

    @api.response(200, 'Review retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Retrieve a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review"""
        data = api.payload

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        try:
            updated = facade.update_review(review_id, data)
            return updated.to_dict(), 200
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        review = facade.delete_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200


# =====================
# /places/<place_id>/reviews
# =====================

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):

    @api.response(200, 'List of reviews for a place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)

        if reviews is None:
            return {'error': 'Place not found'}, 404

        return {'reviews': [review.to_dict() for review in reviews]}, 200

#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services import facade


api = Namespace('users', description='User related operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True,
                           description='Email of the user'),
    'password': fields.String(required=True,
                           description='Password of the user')
})


from flask import request
from flask_restx import Resource

@api.route('/')
class UserList(Resource):
    
    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        if not user_data:
            return {'error': 'Invalid input, JSON expected'}, 400

        required_fields = {'first_name', 'last_name', 'email', 'password'}
        if not required_fields.issubset(user_data):
            return {'error': 'Missing required fields'}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        try:
            new_user = facade.create_user(user_data)

            if not hasattr(new_user, "to_dict"):
                return {'error': 'Internal Server Error', 'details': 'Invalid return type from create_user'}, 500

        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal Server Error', 'details': str(e)}, 500

        return new_user.to_dict(), 201
    def get(self):
        """List all users"""
        users = facade.get_all_users()
        return {'users': [{'id': user.id,
                           'first_name': user.first_name,
                           'last_name': user.last_name,
                           'email': user.email} for user in users]}, 200



@api.route('/<user_id>')
class UserResource(Resource):
    # @api.expect(user_model, validate=True)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email}, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update a user's information"""
        user_data = api.payload
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return {'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email}, 200

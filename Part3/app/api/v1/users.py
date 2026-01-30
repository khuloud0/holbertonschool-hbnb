#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('users', description='User operations')

# ========================
# Models
# ========================

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='User password')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
    'password': fields.String(description='User password')
})

# ========================
# /users
# ========================

@api.route('/')
class UserList(Resource):

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new user"""
        data = api.payload

        if facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400

        try:
            user = facade.create_user(data)
            return user.to_dict(), 201
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        return {'users': [user.to_dict() for user in users]}, 200


# ========================
# /users/<user_id>
# ========================

@api.route('/<user_id>')
class UserResource(Resource):

    @api.response(200, 'User retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Forbidden')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user information"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)

        if not current_user:
            return {'error': 'Unauthorized'}, 403

        data = api.payload

        # 👤 User عادي: يقدر يعدل نفسه فقط
        if not current_user.is_admin:
            if user_id != current_user_id:
                return {'error': 'You can only update your own account'}, 403

            # يمنع تغيير email و password
            data.pop('email', None)
            data.pop('password', None)

        # 👑 Admin: مسموح له كل شيء

        user = facade.update_user(user_id, data)
        if not user:
            return {'error': 'User not found'}, 404

        return user.to_dict(), 200

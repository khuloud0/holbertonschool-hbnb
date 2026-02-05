#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from app.services.facade import facade

api = Namespace(
    'users',
    description='User operations',
    security='Bearer'
)

# ========================
# Models
# ========================

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'is_admin': fields.Boolean(default=False)
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String(),
    'password': fields.String()
})

# ========================
# /users
# ========================

@api.route('/')
class UserList(Resource):

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """
        Create a new user
        - First user can be admin
        - Others require admin privileges
        """
        data = api.payload.copy()

        users = facade.get_all_users()
        is_first_user = len(users) == 0

        # إذا مو أول مستخدم → لازم Admin
        if not is_first_user:
            current_user_id = get_jwt_identity()
            current_user = facade.get_user(current_user_id)

            if not current_user or not current_user.is_admin:
                return {'error': 'Admin privileges required'}, 403

        # تشفير كلمة المرور
        data['password_hash'] = generate_password_hash(
            data.pop('password')
        )

        try:
            user = facade.create_user(data)
            return user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        users = facade.get_all_users()
        return {'users': [u.to_dict() for u in users]}, 200


# ========================
# /users/<user_id>
# ========================

@api.route('/<user_id>')
class UserResource(Resource):

    @api.response(200, 'User retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, user_id):
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)

        if not current_user:
            return {'error': 'Admin privileges required'}, 403

        data = api.payload.copy()

        # User عادي: يعدل نفسه فقط
        if not current_user.is_admin:
            if user_id != current_user_id:
                return {'error': 'Admin privileges required'}, 403

            data.pop('email', None)
            data.pop('password', None)

        # Admin: يقدر يغير كلمة المرور
        if current_user.is_admin and 'password' in data:
            data['password_hash'] = generate_password_hash(
                data.pop('password')
            )

        user = facade.update_user(user_id, data)
        if not user:
            return {'error': 'User not found'}, 404

        return user.to_dict(), 200

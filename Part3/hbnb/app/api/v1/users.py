#!/usr/bin/python3
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required

from app.services.facade import HBnBFacade

api = Namespace("users", description="User operations")
facade = HBnBFacade()

# Response model (NO password/password_hash)
user_model = api.model("User", {
    "id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "is_admin": fields.Boolean,
})

# Create user request model (includes password)
user_create_model = api.model("UserCreate", {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "is_admin": fields.Boolean(required=False),
})

# Login request model
login_model = api.model("Login", {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})


@api.route("/")
class UsersResource(Resource):
    @api.marshal_list_with(user_model)
    @jwt_required()
    def get(self):
        return facade.list_users(), 200

    @api.expect(user_create_model, validate=True)
    @api.marshal_with(user_model, code=201)
    def post(self):
        data = request.get_json() or {}
        user = facade.create_user(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            is_admin=data.get("is_admin", False),
        )
        return user, 201


@api.route("/<string:user_id>")
class UserResource(Resource):
    @api.marshal_with(user_model)
    @jwt_required()
    def get(self, user_id):
        user = facade.get_user(user_id)
        if user is None:
            api.abort(404, "User not found")
        return user, 200


@api.route("/login")
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        data = request.get_json() or {}
        user = facade.get_user_by_email(data["email"])

        if user is None or not user.check_password(data["password"]):
            api.abort(401, "Invalid credentials")

        token = create_access_token(
            identity=user.id,
            additional_claims={"is_admin": user.is_admin}
        )
        return {"access_token": token}, 200

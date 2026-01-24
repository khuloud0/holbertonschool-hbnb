#!/usr/bin/python3
"""HBnB app factory."""

from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns

from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # bcrypt
    bcrypt = Bcrypt(app)
    app.extensions["bcrypt"] = bcrypt

    # jwt
    jwt = JWTManager(app)
    app.extensions["jwt"] = jwt

    api = Api(app, version="1.0", title="HBnB API", description="HBnB API")

    # ONLY namespaces that exist in your structure
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")

    return app

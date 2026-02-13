#!/usr/bin/python3
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_cors import CORS

from config import DevelopmentConfig
from app.db import db

# مهم جداً استيراد المودلز عشان create_all ينشئ الجداول
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

from app.api.v1.users import api as users_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns


bcrypt = Bcrypt()
jwt = JWTManager()

# Swagger JWT Authorizations
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'JWT Authorization header. Example: Bearer <access_token>'
    }
}


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)

    # ✅ حل مشكلة 308 (trailing slash)
    app.url_map.strict_slashes = False

    app.config.from_object(config_class)

    # ✅ حل مشكلة CORS بين Part4 و Part3
    CORS(app)

    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # إنشاء الجداول
    with app.app_context():
        db.create_all()

    api = Api(
        app,
        title="HBnB API",
        version="1.0",
        description="HBnB Application API",
        authorizations=authorizations,
        security='Bearer'
    )

    # Register namespaces
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")

    return app

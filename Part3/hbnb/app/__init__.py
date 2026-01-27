#!/usr/bin/python3
"""HBnB app factory with authentication and admin support."""

from flask import Flask, jsonify
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.admin import api as admin_ns

from config import Config


@JWTManager.user_identity_loader
def user_identity_lookup(user):
    return user.id if hasattr(user, 'id') else user

@JWTManager.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    from app.models.user import User
    from app import db
    identity = jwt_data["sub"]
    return db.users_by_id.get(identity)

@JWTManager.additional_claims_loader
def add_claims_to_access_token(identity):
    from app.models.user import User
    from app import db
    user = db.users_by_id.get(identity)
    if user:
        return {"is_admin": user.is_admin}
    return {"is_admin": False}

@JWTManager.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"error": "Token has expired", "authenticated": False}), 401

@JWTManager.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Invalid token", "authenticated": False}), 401

@JWTManager.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"error": "Authorization required", "authenticated": False}), 401


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    app.config['JWT_SECRET_KEY'] = app.config.get('JWT_SECRET_KEY', 'super-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=app.config.get('JWT_ACCESS_TOKEN_EXPIRES_HOURS', 24))
    
    bcrypt = Bcrypt(app)
    app.extensions["bcrypt"] = bcrypt

    jwt = JWTManager(app)
    app.extensions["jwt"] = jwt

    api = Api(
        app, 
        version="1.0", 
        title="HBnB API", 
        description="HBnB API with JWT Authentication & Admin Support",
        doc="/api/v1/docs",
        authorizations={
            'Bearer Auth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': "Type in the value input box: **Bearer {your JWT token}**"
            }
        },
        security='Bearer Auth'
    )

    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(admin_ns, path="/api/v1/admin")

    @app.route('/api/v1/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy",
            "version": "1.0",
            "features": {
                "authentication": True,
                "authorization": True,
                "admin_support": True
            }
        }), 200

    @app.route('/api/v1/test-jwt', methods=['GET'])
    @jwt_required()
    def test_jwt():
        from flask_jwt_extended import get_jwt_identity
        current_user_id = get_jwt_identity()
        return jsonify({
            "message": "JWT is working correctly",
            "user_id": current_user_id
        }), 200

    @app.route('/api/v1/test-admin', methods=['GET'])
    @jwt_required()
    def test_admin():
        from flask_jwt_extended import get_jwt
        claims = get_jwt()
        return jsonify({
            "message": "Admin check endpoint",
            "is_admin": claims.get('is_admin', False),
            "claims": claims
        }), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    with app.app_context():
        from app import db
        from app.models.user import User
        
        admin_email = app.config.get('DEFAULT_ADMIN_EMAIL', 'admin@hbnb.com')
        admin_password = app.config.get('DEFAULT_ADMIN_PASSWORD', 'admin123')
        
        admin_exists = False
        for user in db.users.values():
            if hasattr(user, 'email') and user.email == admin_email:
                admin_exists = True
                break
        
        if not admin_exists:
            try:
                admin_user = User(
                    first_name="Admin",
                    last_name="User",
                    email=admin_email,
                    password=admin_password,
                    is_admin=True
                )
                
                db.users[admin_user.email] = admin_user
                db.users_by_id[admin_user.id] = admin_user
                
                print(f"Created default admin user: {admin_email}")
                
            except Exception as e:
                print(f"Could not create admin user: {e}")

    return app

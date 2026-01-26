#!/usr/bin/python3
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

#!/usr/bin/python3
"""User model with bcrypt password hashing and JWT authentication support."""

import re
from flask import current_app
from app.models.base_model import BaseModel
from flask_jwt_extended import create_access_token
from datetime import timedelta

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel):
    def __init__(self, first_name: str, last_name: str, email: str, password: str, is_admin: bool = False):
        super().__init__()
        self.first_name = self._required_str(first_name, "first_name", 50)
        self.last_name = self._required_str(last_name, "last_name", 50)
        self.email = self._email(email)
        self.is_admin = bool(is_admin)
        self.password_hash = self._hash_password(password)
        self.places = []  # For relationship with places
        self.reviews = []  # For relationship with reviews

    @staticmethod
    def _required_str(value: str, field: str, max_len: int) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{field} must be a string")
        cleaned = value.strip()
        if cleaned == "":
            raise ValueError(f"{field} is required")
        if len(cleaned) > max_len:
            raise ValueError(f"{field} must be at most {max_len} characters")
        return cleaned

    @staticmethod
    def _email(value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("email must be a string")
        cleaned = value.strip().lower()
        if cleaned == "":
            raise ValueError("email is required")
        if not _EMAIL_RE.match(cleaned):
            raise ValueError("email format is invalid")
        return cleaned

    @staticmethod
    def _hash_password(password: str) -> str:
        if not isinstance(password, str):
            raise TypeError("password must be a string")
        if password.strip() == "":
            raise ValueError("password is required")

        bcrypt = current_app.extensions["bcrypt"]
        return bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        bcrypt = current_app.extensions["bcrypt"]
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_days: int = 1):
        """Generate JWT token for this user (Task 3 requirement)"""
        from flask_jwt_extended import create_access_token
        return create_access_token(
            identity=self.id,
            expires_delta=timedelta(days=expires_days),
            additional_claims={'is_admin': self.is_admin}
        )

    def can_modify(self, resource_user_id: str) -> bool:
        """Check if user can modify a resource (Task 3 requirement)"""
        # User can modify if they own the resource OR they are admin (Task 4 requirement)
        return str(self.id) == str(resource_user_id) or self.is_admin

    def can_review_place(self, place_owner_id: str) -> bool:
        """Check if user can review a place (Task 3 requirement)"""
        # User cannot review their own place
        return str(self.id) != str(place_owner_id)

    def to_dict(self, include_sensitive: bool = False) -> dict:
        """Convert user to dictionary (Task 3 & 4 requirement)"""
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            'updated_at': self.updated_at.isoformat() if hasattr(self, 'updated_at') else None
        }
        
        if include_sensitive:
            data['password_hash'] = self.password_hash
            
        return data

    @classmethod
    def authenticate(cls, email: str, password: str):
        """Authenticate user and return user object if valid (Task 3 requirement)"""
        from app import db
        user = db.users.get(email)
        if user and user.check_password(password):
            return user
        return None

    def update_profile(self, data: dict, current_user=None) -> dict:
        """
        Update user profile with validation (Task 3 & 4 requirement)
        - Regular users can update their own info (except email and is_admin)
        - Admins can update any user's info
        """
        from app import db
        
        # Determine if current user has admin privileges
        is_admin = current_user.is_admin if current_user else self.is_admin
        is_self = current_user and str(current_user.id) == str(self.id)
        
        updates = {}
        errors = []
        
        # Check first_name
        if 'first_name' in data:
            try:
                updates['first_name'] = self._required_str(data['first_name'], "first_name", 50)
            except (TypeError, ValueError) as e:
                errors.append(str(e))
        
        # Check last_name
        if 'last_name' in data:
            try:
                updates['last_name'] = self._required_str(data['last_name'], "last_name", 50)
            except (TypeError, ValueError) as e:
                errors.append(str(e))
        
        # Email updates - only allowed by admin or if updating self without changing email
        if 'email' in data:
            if is_admin or (is_self and data['email'] == self.email):
                try:
                    new_email = self._email(data['email'])
                    # Check if email already exists (except for current user)
                    existing = db.users.get(new_email)
                    if existing and str(existing.id) != str(self.id):
                        errors.append("Email already exists")
                    else:
                        updates['email'] = new_email
                except (TypeError, ValueError) as e:
                    errors.append(str(e))
            else:
                errors.append("Only admins can change email addresses")
        
        # Password updates - allowed by admin or user themselves
        if 'password' in data:
            if is_admin or is_self:
                try:
                    updates['password_hash'] = self._hash_password(data['password'])
                except (TypeError, ValueError) as e:
                    errors.append(str(e))
            else:
                errors.append("Cannot change another user's password")
        
        # is_admin updates - only allowed by admin
        if 'is_admin' in data:
            if is_admin:
                updates['is_admin'] = bool(data['is_admin'])
            else:
                errors.append("Only admins can change admin status")
        
        if errors:
            return {'success': False, 'errors': errors}
        
        # Apply updates
        for key, value in updates.items():
            setattr(self, key, value)
        
        self.updated_at = datetime.utcnow()
        return {'success': True, 'user': self}

    def is_resource_owner(self, resource) -> bool:
        """Check if user owns a resource (Task 3 requirement)"""
        if hasattr(resource, 'user_id'):
            return str(self.id) == str(resource.user_id)
        elif hasattr(resource, 'author_id'):
            return str(self.id) == str(resource.author_id)
        return False

    def get_accessible_resources(self, resource_type: str):
        """Get resources accessible to user (Task 3 & 4 requirement)"""
        from app import db
        
        if resource_type == 'places':
            if self.is_admin:
                return list(db.places.values())
            return [place for place in db.places.values() if str(place.user_id) == str(self.id)]
        
        elif resource_type == 'reviews':
            if self.is_admin:
                return list(db.reviews.values())
            return [review for review in db.reviews.values() if str(review.user_id) == str(self.id)]
        
        return []

    @classmethod
    def create_admin(cls, email: str, password: str, first_name: str = "Admin", last_name: str = "User"):
        """Create an admin user (Task 4 requirement)"""
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_admin=True
        )

#!/usr/bin/python3
"""User model"""

import re
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base_model import BaseModel
from app.db import db


class User(BaseModel):
    """User SQLAlchemy model"""

    __tablename__ = "users"

    # ===== Columns =====
    email = db.Column(db.String(128), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # ===== Init =====
    def __init__(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        is_admin: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)

        # ---- validations ----
        self._validate_name(first_name, "first_name")
        self._validate_name(last_name, "last_name")
        self._validate_email(email)

        # ---- assign values ----
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

        # ---- password hashing ----
        self.password_hash = generate_password_hash(password)

    # ===== Password helpers =====
    def check_password(self, password: str) -> bool:
        """Verify password"""
        return check_password_hash(self.password_hash, password)

    # ===== Validation Helpers =====
    def _validate_name(self, value: str, field: str):
        if not value or not isinstance(value, str):
            raise ValueError(f"{field} is required")
        if len(value) > 50:
            raise ValueError(f"{field} must be at most 50 characters")

    def _validate_email(self, email: str):
        if not email or not isinstance(email, str):
            raise ValueError("email is required")

        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")

    # ===== Serialization =====
    def to_dict(self):
        """Dictionary representation (safe)"""
        data = super().to_dict()
        data.update({
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_admin": self.is_admin
        })
        return data

#!/usr/bin/python3
"""User model with bcrypt password hashing (no circular imports)."""

import re
from flask import current_app
from app.models.base_model import BaseModel

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel):
    def __init__(self, first_name: str, last_name: str, email: str, password: str, is_admin: bool = False):
        super().__init__()
        self.first_name = self._required_str(first_name, "first_name", 50)
        self.last_name = self._required_str(last_name, "last_name", 50)
        self.email = self._email(email)
        self.is_admin = bool(is_admin)
        self.password_hash = self._hash_password(password)

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


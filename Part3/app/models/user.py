#!/usr/bin/python3
"""User model"""

import re
from werkzeug.security import generate_password_hash
from app.models.base_model import BaseModel


class User(BaseModel):
    """User class"""

    used_emails = set()  # in-memory uniqueness check

    def __init__(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str = "",
        is_admin: bool = False
    ):
        super().__init__()

        # ---- validations ----
        self._validate_name(first_name, "first_name")
        self._validate_name(last_name, "last_name")
        self._validate_email(email)

        if email in User.used_emails:
            raise ValueError("Email already exists")

        # ---- assign values ----
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

        # ---- password hashing ----
        self.password_hash = (
            generate_password_hash(password)
            if password else ""
        )

        User.used_emails.add(email)

    # ---------- Validation Helpers ----------

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

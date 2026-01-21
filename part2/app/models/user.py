#!/usr/bin/python3
"""User model"""

from flask_bcrypt import generate_password_hash
from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, email: str, first_name: str = "", last_name: str = "",
                 password: str = "", is_admin: bool = False):
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = (
            generate_password_hash(password).decode("utf-8")
            if password else ""
        )
        self.is_admin = is_admin

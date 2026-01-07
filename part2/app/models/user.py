#!/usr/bin/python3

from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, email: str, first_name: str = "", last_name: str = "", password: str = "", is_admin: bool = False):
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_admin = is_admin

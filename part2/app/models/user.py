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

        # Merge dictionaries, excluding password
        return {**base_dict, **user_dict}
    
    def to_dict_with_password(self):
        """Convert user to dictionary (include password - for internal use)"""
        base_dict = super().to_dict()
        user_dict = {
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name
        }
        return {**base_dict, **user_dict}
    
    def update(self, data: dict):
        """Update user attributes"""
        allowed_fields = ['email', 'first_name', 'last_name']
        for field in allowed_fields:
            if field in data:
                setattr(self, field, data[field])
        super().save()
        return self
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create user instance from dictionary"""
        return cls(
            email=data.get('email', ''),
            password=data.get('password', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )

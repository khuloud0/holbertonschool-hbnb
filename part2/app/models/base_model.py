#!/usr/bin/python3
"""BaseModel module"""

import uuid
from datetime import datetime


class BaseModel:
    """Base class for all models"""

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", str(uuid.uuid4()))

        # created_at
        created_at = kwargs.get("created_at")
        if isinstance(created_at, str):
            self.created_at = datetime.fromisoformat(created_at)
        else:
            self.created_at = created_at if created_at else datetime.utcnow()

        # updated_at
        updated_at = kwargs.get("updated_at")
        if isinstance(updated_at, str):
            self.updated_at = datetime.fromisoformat(updated_at)
        else:
            self.updated_at = updated_at if updated_at else self.created_at

    def save(self):
        """Update updated_at timestamp"""
        self.updated_at = datetime.utcnow()

    def update(self, data: dict):
        """
        Update instance attributes then call save()
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")

        protected_fields = {"id", "created_at", "updated_at"}

        for key, value in data.items():
            if key in protected_fields:
                continue
            if hasattr(self, key):
                setattr(self, key, value)

        self.save()

    def to_dict(self):
        """Dictionary representation of the instance"""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

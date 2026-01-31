#!/usr/bin/python3
"""BaseModel module"""

import uuid
from datetime import datetime
from app.db import db


class BaseModel(db.Model):
    """Base class for all SQLAlchemy models"""

    __abstract__ = True

    id = db.Column(
        db.String(60),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __init__(self, **kwargs):
        """
        Initialize model with keyword arguments
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def save(self):
        """Save the current instance"""
        db.session.add(self)
        db.session.commit()

    def update(self, data: dict):
        """Update instance attributes then save"""
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
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

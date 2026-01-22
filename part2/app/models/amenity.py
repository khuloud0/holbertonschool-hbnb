#!/usr/bin/python3
"""Amenity model"""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class"""

    def __init__(self, name: str):
        super().__init__()

        # ---- validation ----
        self._validate_name(name)

        # ---- assign value ----
        self.name = name

    def _validate_name(self, name):
        if not name or not isinstance(name, str):
            raise ValueError("name is required")
        if len(name) > 50:
            raise ValueError("name must be at most 50 characters")

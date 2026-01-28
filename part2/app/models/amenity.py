#!/usr/bin/python3
"""Amenity model"""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class"""

    def __init__(self, name: str, description: str = "", **kwargs):
        super().__init__()

        # ---- validations ----
        self._validate_name(name)
        self._validate_description(description)

        # ---- assign values ----
        self.name = name
        self.description = description

    # ---------- Validation Helpers ----------

    def _validate_name(self, name: str):
        if not name or not isinstance(name, str):
            raise ValueError("name is required")
        if len(name) > 50:
            raise ValueError("name must be at most 50 characters")

    def _validate_description(self, description: str):
        if not description or not isinstance(description, str):
            raise ValueError("description is required")
        if len(description) > 255:
            raise ValueError("description must be at most 255 characters")

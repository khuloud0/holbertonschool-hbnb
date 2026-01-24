#!/usr/bin/python3
"""Amenity model with validations."""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name: str):
        super().__init__()
        self.name = self._required_str(name, "name", 50)

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

#!/usr/bin/python3
"""Place model with validations, relationships, and methods."""

from typing import List
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    def __init__(
        self,
        title: str,
        owner: User,
        description: str = "",
        price: float = 1.0,
        latitude: float = 0.0,
        longitude: float = 0.0
    ):
        super().__init__()
        self.title = self._required_str(title, "title", 100)
        self.description = description if isinstance(description, str) else ""
        self.price = self._positive_float(price, "price")
        self.latitude = self._range_float(latitude, "latitude", -90.0, 90.0)
        self.longitude = self._range_float(longitude, "longitude", -180.0, 180.0)
        self.owner = self._owner(owner)

        # required relationship containers
        self.reviews: List["Review"] = []
        self.amenities: List[Amenity] = []

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
    def _positive_float(value, field: str) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{field} must be a float")
        val = float(value)
        if val <= 0:
            raise ValueError(f"{field} must be positive")
        return val

    @staticmethod
    def _range_float(value, field: str, min_v: float, max_v: float) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{field} must be a float")
        val = float(value)
        if val < min_v or val > max_v:
            raise ValueError(f"{field} must be between {min_v} and {max_v}")
        return val

    @staticmethod
    def _owner(owner: User) -> User:
        if not isinstance(owner, User):
            raise TypeError("owner must be a User instance")
        return owner

    def add_review(self, review: "Review") -> None:
        from app.models.review import Review  # local import avoids circular import
        if not isinstance(review, Review):
            raise TypeError("review must be a Review instance")
        if review.place is not self:
            raise ValueError("review.place must reference this Place")
        if review in self.reviews:
            return
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity: Amenity) -> None:
        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity instance")
        if amenity in self.amenities:
            return
        self.amenities.append(amenity)
        self.save()

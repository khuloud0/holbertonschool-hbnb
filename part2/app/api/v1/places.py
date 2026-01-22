#!/usr/bin/python3
"""Place model"""

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity


class Place(BaseModel):
    """Place class"""

    def __init__(
        self,
        title: str,
        owner: User,
        description: str = "",
        price: float = 0.0,
        latitude: float = 0.0,
        longitude: float = 0.0
    ):
        super().__init__()

        # ---------- validations ----------
        self._validate_title(title)
        self._validate_price(price)
        self._validate_latitude(latitude)
        self._validate_longitude(longitude)
        self._validate_owner(owner)

        # ---------- assign values ----------
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        # ---------- relationships ----------
        self.reviews = []
        self.amenities = []

    # ---------- Validation Helpers ----------

    def _validate_title(self, title):
        if not title or not isinstance(title, str):
            raise ValueError("title is required")
        if len(title) > 100:
            raise ValueError("title must be at most 100 characters")

    def _validate_price(self, price):
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("price must be a positive number")

    def _validate_latitude(self, latitude):
        if not isinstance(latitude, (int, float)):
            raise ValueError("latitude must be a number")
        if latitude < -90 or latitude > 90:
            raise ValueError("latitude must be between -90 and 90")

    def _validate_longitude(self, longitude):
        if not isinstance(longitude, (int, float)):
            raise ValueError("longitude must be a number")
        if longitude < -180 or longitude > 180:
            raise ValueError("longitude must be between -180 and 180")

    def _validate_owner(self, owner):
        if not isinstance(owner, User):
            raise ValueError("owner must be a User instance")

    # ---------- Relationship Methods ----------

    def add_review(self, review):
        """Attach a review to this place"""
        if not isinstance(review, Review):
            raise ValueError("review must be a Review instance")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Attach an amenity to this place"""
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")
        self.amenities.append(amenity)

#!/usr/bin/python3
"""Review model"""

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place
from datetime import datetime


class Review(BaseModel):
    """Review class"""

    def __init__(
        self,
        text: str,
        rating: int,
        user: User,
        place: Place
    ):
        super().__init__()

        # ---- validations ----
        self._validate_text(text)
        self._validate_rating(rating)
        self._validate_user(user)
        self._validate_place(place)

        # ---- assign values ----
        self.text = text
        self.rating = rating
        self.user = user
        self.place = place

        # link review to place
        place.add_review(self)

    # ---------- Update ----------

    def update(self, **kwargs):
        if "text" in kwargs:
            self._validate_text(kwargs["text"])
            self.text = kwargs["text"]

        if "rating" in kwargs:
            self._validate_rating(kwargs["rating"])
            self.rating = kwargs["rating"]

        self.updated_at = datetime.utcnow()

    # ---------- Validation Helpers ----------

    def _validate_text(self, text):
        if not text or not isinstance(text, str):
            raise ValueError("text is required")

    def _validate_rating(self, rating):
        if not isinstance(rating, int):
            raise ValueError("rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")

    def _validate_user(self, user):
        if not isinstance(user, User):
            raise ValueError("user must be a User instance")

    def _validate_place(self, place):
        if not isinstance(place, Place):
            raise ValueError("place must be a Place instance")

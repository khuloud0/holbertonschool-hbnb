#!/usr/bin/python3
"""Review model with validations and references."""

from app.models.base_model import BaseModel
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text: str, rating: int, user: User, place):
        super().__init__()
        self.text = self._required_text(text)
        self.rating = self._rating(rating)
        self.user = self._user(user)
        self.place = self._place(place)

    @staticmethod
    def _required_text(value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("text must be a string")
        cleaned = value.strip()
        if cleaned == "":
            raise ValueError("text is required")
        return cleaned

    @staticmethod
    def _rating(value: int) -> int:
        if not isinstance(value, int):
            raise TypeError("rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("rating must be between 1 and 5")
        return value

    @staticmethod
    def _user(user: User) -> User:
        if not isinstance(user, User):
            raise TypeError("user must be a User instance")
        return user

    @staticmethod
    def _place(place):
        from app.models.place import Place  # local import avoids circular import
        if not isinstance(place, Place):
            raise TypeError("place must be a Place instance")
        return place

#!/usr/bin/python3
"""Facade connecting API layer to persistence + models."""

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.repo = InMemoryRepository()

    # ----------------
    # Users
    # ----------------
    def create_user(self, first_name: str, last_name: str, email: str, password: str, is_admin: bool = False) -> User:
        user = User(first_name=first_name, last_name=last_name, email=email, password=password, is_admin=is_admin)
        return self.repo.add(user)

    def get_user(self, user_id: str):
        return self.repo.get("User", user_id)

    def list_users(self):
        return self.repo.all("User")

    def get_user_by_email(self, email: str):
        return self.repo.find_user_by_email(email)

    # ----------------
    # Amenities
    # ----------------
    def create_amenity(self, name: str) -> Amenity:
        amenity = Amenity(name=name)
        return self.repo.add(amenity)

    def get_amenity(self, amenity_id: str):
        return self.repo.get("Amenity", amenity_id)

    def list_amenities(self):
        return self.repo.all("Amenity")

    # ----------------
    # Places
    # ----------------
    def create_place(
        self,
        title: str,
        owner: User,
        description: str = "",
        price: float = 1.0,
        latitude: float = 0.0,
        longitude: float = 0.0
    ) -> Place:
        place = Place(
            title=title,
            owner=owner,
            description=description,
            price=price,
            latitude=latitude,
            longitude=longitude,
        )
        return self.repo.add(place)

    def get_place(self, place_id: str):
        return self.repo.get("Place", place_id)

    def list_places(self):
        return self.repo.all("Place")

    # ----------------
    # Reviews
    # ----------------
    def create_review(self, text: str, rating: int, user: User, place: Place) -> Review:
        review = Review(text=text, rating=rating, user=user, place=place)
        self.repo.add(review)
        place.add_review(review)  # maintain relationship integrity
        return review

    def get_review(self, review_id: str):
        return self.repo.get("Review", review_id)

    def list_reviews(self):
        return self.repo.all("Review")

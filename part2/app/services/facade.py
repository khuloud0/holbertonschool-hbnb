#!/usr/bin/python3
"""Facade layer for HBnB application"""

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from datetime import datetime


class HBnBFacade:
    """Facade class handling business logic"""

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ================= USERS =================

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        users = self.user_repo.get_all()
        for user in users:
            if user.email == email:
                return user
        return None

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        for key in ["first_name", "last_name", "email", "password"]:
            if key in user_data:
                setattr(user, key, user_data[key])

        user.updated_at = datetime.utcnow()
        self.user_repo.update(user_id, user_data)
        return user

    # ================= PLACES =================

    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        owner = self.user_repo.get(owner_id)

        if not owner:
            raise ValueError("Owner not found")

        place_data["owner"] = owner
        place_data.pop("owner_id")

        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        for key in ["title", "description", "price", "latitude", "longitude"]:
            if key in place_data:
                setattr(place, key, place_data[key])

        self.place_repo.update(place_id, place_data)
        return place

      # ================== AMENITIES ==================

def create_amenity(self, amenity_data):
    if "name" not in amenity_data:
        raise ValueError("Amenity name is required")

    if "description" not in amenity_data:
        raise ValueError("Amenity description is required")

    amenity = Amenity(
        name=amenity_data["name"],
        description=amenity_data["description"]
    )

    self.amenity_repo.add(amenity)
    return amenity


def get_amenity(self, amenity_id):
    return self.amenity_repo.get(amenity_id)


def get_all_amenities(self):
    return self.amenity_repo.get_all()


def update_amenity(self, amenity_id, amenity_data):
    amenity = self.amenity_repo.get(amenity_id)
    if not amenity:
        return None

    if "name" in amenity_data:
        if not amenity_data["name"]:
            raise ValueError("Amenity name is required")
        amenity.name = amenity_data["name"]

    if "description" in amenity_data:
        if not amenity_data["description"]:
            raise ValueError("Amenity description is required")
        amenity.description = amenity_data["description"]

    self.amenity_repo.update(amenity_id, amenity_data)
    return amenity

    # ================= REVIEWS =================

    def create_review(self, review_data):
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        review_data["user"] = user
        review_data["place"] = place
        review_data.pop("user_id")
        review_data.pop("place_id")

        review = Review(**review_data)
        self.review_repo.add(review)

        place.add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if "text" in review_data:
            review._validate_text(review_data["text"])
            review.text = review_data["text"]

        if "rating" in review_data:
            review._validate_rating(review_data["rating"])
            review.rating = review_data["rating"]

        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        self.review_repo.delete(review_id)
        return review


# Facade instance
facade = HBnBFacade()

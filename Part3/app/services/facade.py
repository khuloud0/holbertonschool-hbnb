#!/usr/bin/python3
"""Facade layer for HBnB application"""

from datetime import datetime

from app.repositories.user_repository import UserRepository
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """Facade class handling business logic"""

    def __init__(self):
        # SQLAlchemy repositories (Part 3)
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # ================= USERS =================

    def create_user(self, user_data):
        if self.user_repo.get_by_email(user_data.get("email")):
            raise ValueError("Email already exists")

        user = User(**user_data)
        return self.user_repo.add(user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_email(email)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        for key in ["first_name", "last_name", "email"]:
            if key in user_data:
                setattr(user, key, user_data[key])

        user.updated_at = datetime.utcnow()
        return self.user_repo.update(user)

    # ================= PLACES =================

    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        place = Place(**place_data)
        return self.place_repo.add(place)

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

        place.updated_at = datetime.utcnow()
        return self.place_repo.update(place)

    # ================= AMENITIES =================

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        for key in ["name", "description"]:
            if key in amenity_data:
                setattr(amenity, key, amenity_data[key])

        amenity.updated_at = datetime.utcnow()
        return self.amenity_repo.update(amenity)

    # ================= REVIEWS =================

    def create_review(self, review_data):
        user = self.user_repo.get(review_data.get("user_id"))
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(review_data.get("place_id"))
        if not place:
            raise ValueError("Place not found")

        # نخلي user_id و place_id تنحفظ مباشرة
        review = Review(**review_data)
        return self.review_repo.add(review)

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        review.update(review_data)
        return self.review_repo.update(review)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        self.review_repo.delete(review_id)
        return review


# Facade instance
facade = HBnBFacade()

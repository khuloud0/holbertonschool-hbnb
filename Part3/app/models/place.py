#!/usr/bin/python3
"""Place model"""

from app.db import db
from app.models.base_model import BaseModel
from app.models.place_amenity import place_amenity


class Place(BaseModel):
    """Place class"""

    __tablename__ = "places"

    # ======================
    # Columns
    # ======================

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)

    owner_id = db.Column(
        db.String(60),
        db.ForeignKey("users.id"),
        nullable=False
    )

    # ======================
    # Relationships
    # ======================

    reviews = db.relationship(
        "Review",
        backref="place",
        cascade="all, delete-orphan",
        lazy=True
    )

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        backref="places",
        lazy="subquery"
    )

    # ======================
    # Serialization
    # ======================

    def to_dict(self):
        """Dictionary representation for frontend"""

        data = super().to_dict()

        # Calculate average rating
        if self.reviews:
            avg_rating = sum(review.rating for review in self.reviews) / len(self.reviews)
        else:
            avg_rating = 0

        data.update({
            "name": self.title,
            "description": self.description,
            "price_per_night": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city": self.city,
            "country": self.country,
            "average_rating": round(avg_rating, 1),

            # 👇 Amenities list
            "amenities": [
                {
                    "id": amenity.id,
                    "name": amenity.name
                }
                for amenity in self.amenities
            ]
        })

        return data

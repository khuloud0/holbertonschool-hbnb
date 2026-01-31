#!/usr/bin/python3
"""Place model"""

from app.db import db
from app.models.base_model import BaseModel
from app.models.place_amenity import place_amenity


class Place(BaseModel):
    """Place class"""

    __tablename__ = "places"

    # ===== Columns =====
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # ===== Foreign Keys =====
    owner_id = db.Column(
        db.String(60),
        db.ForeignKey("users.id"),
        nullable=False
    )

    # ===== Relationships =====
    reviews = db.relationship(
        "Review",
        backref="place",
        cascade="all, delete-orphan"
    )

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        backref="places",
        lazy="subquery"
    )

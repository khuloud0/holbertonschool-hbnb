#!/usr/bin/python3
"""Review model"""

from app.db import db
from app.models.base_model import BaseModel


class Review(BaseModel, db.Model):
    """Review class"""

    __tablename__ = "reviews"

    # ===== Columns =====
    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # ===== Foreign Keys =====
    user_id = db.Column(
        db.String(60),
        db.ForeignKey("users.id"),
        nullable=False
    )

    place_id = db.Column(
        db.String(60),
        db.ForeignKey("places.id"),
        nullable=False
    )

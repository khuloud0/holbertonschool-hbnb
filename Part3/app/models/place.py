#!/usr/bin/python3
"""Place model"""

from app.db import db
from app.models.base_model import BaseModel


class Place(BaseModel, db.Model):
    """Place class"""

    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

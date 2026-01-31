#!/usr/bin/python3
from app.db import db
from app.models.base_model import BaseModel


class Amenity(BaseModel, db.Model):
    __tablename__ = "amenities"

    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False)

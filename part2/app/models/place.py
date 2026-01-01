#!/usr/bin/python3
from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title="", description="", price=0.0,
                 latitude=0.0, longitude=0.0, owner_id=""):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

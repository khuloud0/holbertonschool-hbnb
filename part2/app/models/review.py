#!/usr/bin/python3

from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text: str, user_id: str, place_id: str):
        super().__init__()
        self.text = text
        self.user_id = user_id
        self.place_id = place_id

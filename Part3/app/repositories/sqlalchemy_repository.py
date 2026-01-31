#!/usr/bin/python3
"""
SQLAlchemy Repository
"""

from app.db import db


class SQLAlchemyRepository:
    """Generic repository using SQLAlchemy"""

    def __init__(self, model):
        self.model = model

    def add(self, obj):
        """Add object to database"""
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """Get object by ID"""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Get all objects"""
        return self.model.query.all()

    def update(self, obj):
        """Update object"""
        db.session.commit()
        return obj

    def delete(self, obj_id):
        """Delete object"""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
        return obj

#!/usr/bin/python3
"""Base model for SQLAlchemy integration."""

from datetime import datetime
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()
Base = declarative_base()


class BaseModel(Base):
    """Base model class for SQLAlchemy."""
    
    __abstract__ = True
    
    id = Column(String(60), primary_key=True, default=lambda: str(uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, 
                       onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, *args, **kwargs):
        """Initialize base model."""
        super().__init__(*args, **kwargs)
        if not self.id:
            self.id = str(uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def save(self):
        """Save the model to the database."""
        try:
            self.updated_at = datetime.utcnow()
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Delete the model from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get(cls, obj_id):
        """Get object by ID."""
        return cls.query.get(obj_id)
    
    @classmethod
    def all(cls):
        """Get all objects."""
        return cls.query.all()
    
    @classmethod
    def count(cls):
        """Count all objects."""
        return cls.query.count()
    
    @classmethod
    def filter_by(cls, **kwargs):
        """Filter objects by criteria."""
        return cls.query.filter_by(**kwargs).all()
    
    @classmethod
    def first(cls, **kwargs):
        """Get first object matching criteria."""
        return cls.query.filter_by(**kwargs).first()

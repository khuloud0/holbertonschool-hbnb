#!/usr/bin/python3
"""SQLAlchemy repository implementation for Task 5."""

from typing import List, Optional, Dict, Any, Type, TypeVar
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from .base_repository import BaseRepository

db = SQLAlchemy()
T = TypeVar('T')


class SQLAlchemyRepository(BaseRepository[T]):
    """SQLAlchemy-based repository for database persistence."""
    
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
    
    def create(self, obj: T) -> T:
        """Create a new object in the database."""
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    def get(self, obj_id: str) -> Optional[T]:
        """Get an object by ID from the database."""
        try:
            return self.model_class.query.get(obj_id)
        except SQLAlchemyError:
            return None
    
    def get_by(self, **kwargs) -> Optional[T]:
        """Get an object by specific criteria from the database."""
        try:
            return self.model_class.query.filter_by(**kwargs).first()
        except SQLAlchemyError:
            return None
    
    def get_all(self) -> List[T]:
        """Get all objects from the database."""
        try:
            return self.model_class.query.all()
        except SQLAlchemyError:
            return []
    
    def update(self, obj_id: str, data: Dict[str, Any]) -> Optional[T]:
        """Update an object in the database."""
        try:
            obj = self.get(obj_id)
            if not obj:
                return None
            
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            
            db.session.commit()
            return obj
        except SQLAlchemyError as e:
            db.session.rollback()
            return None
    
    def delete(self, obj_id: str) -> bool:
        """Delete an object from the database."""
        try:
            obj = self.get(obj_id)
            if not obj:
                return False
            
            db.session.delete(obj)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            return False
    
    def filter_by(self, **kwargs) -> List[T]:
        """Filter objects by criteria from the database."""
        try:
            return self.model_class.query.filter_by(**kwargs).all()
        except SQLAlchemyError:
            return []
    
    def count(self) -> int:
        """Count all objects in the database."""
        try:
            return self.model_class.query.count()
        except SQLAlchemyError:
            return 0
    
    def exists(self, obj_id: str) -> bool:
        """Check if object exists in the database."""
        try:
            return self.model_class.query.get(obj_id) is not None
        except SQLAlchemyError:
            return False
    
    def paginate(self, page: int = 1, per_page: int = 10) -> List[T]:
        """Paginate results from the database."""
        try:
            return self.model_class.query.paginate(
                page=page, per_page=per_page, error_out=False
            ).items
        except SQLAlchemyError:
            return []
    
    def bulk_create(self, objects: List[T]) -> List[T]:
        """Create multiple objects in a single transaction."""
        try:
            db.session.add_all(objects)
            db.session.commit()
            return objects
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute raw SQL query."""
        try:
            result = db.session.execute(query, params or {})
            return [dict(row) for row in result]
        except SQLAlchemyError:
            return []

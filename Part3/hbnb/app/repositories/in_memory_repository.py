#!/usr/bin/python3
"""In-memory repository implementation."""

from typing import List, Optional, Dict, Any, Type
from .base_repository import BaseRepository


class InMemoryRepository(BaseRepository):
    """In-memory repository for development/testing."""
    
    def __init__(self, model_class: Type):
        self.model_class = model_class
        self._storage = {}
    
    def create(self, obj) -> any:
        """Create a new object."""
        obj_id = str(len(self._storage) + 1)
        if hasattr(obj, 'id'):
            obj.id = obj_id
        self._storage[obj_id] = obj
        return obj
    
    def get(self, obj_id: str) -> Optional[any]:
        """Get an object by ID."""
        return self._storage.get(obj_id)
    
    def get_by(self, **kwargs) -> Optional[any]:
        """Get an object by specific criteria."""
        for obj in self._storage.values():
            match = True
            for key, value in kwargs.items():
                if getattr(obj, key, None) != value:
                    match = False
                    break
            if match:
                return obj
        return None
    
    def get_all(self) -> List[any]:
        """Get all objects."""
        return list(self._storage.values())
    
    def update(self, obj_id: str, data: Dict[str, Any]) -> Optional[any]:
        """Update an object."""
        obj = self.get(obj_id)
        if not obj:
            return None
        
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        
        return obj
    
    def delete(self, obj_id: str) -> bool:
        """Delete an object."""
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False
    
    def filter_by(self, **kwargs) -> List[any]:
        """Filter objects by criteria."""
        results = []
        for obj in self._storage.values():
            match = True
            for key, value in kwargs.items():
                if getattr(obj, key, None) != value:
                    match = False
                    break
            if match:
                results.append(obj)
        return results
    
    def count(self) -> int:
        """Count all objects."""
        return len(self._storage)
    
    def exists(self, obj_id: str) -> bool:
        """Check if object exists."""
        return obj_id in self._storage

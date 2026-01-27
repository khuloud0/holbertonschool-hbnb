#!/usr/bin/python3
"""Base repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, TypeVar, Generic

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Abstract base class for all repositories."""
    
    @abstractmethod
    def create(self, obj: T) -> T:
        """Create a new object."""
        pass
    
    @abstractmethod
    def get(self, obj_id: str) -> Optional[T]:
        """Get an object by ID."""
        pass
    
    @abstractmethod
    def get_by(self, **kwargs) -> Optional[T]:
        """Get an object by specific criteria."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all objects."""
        pass
    
    @abstractmethod
    def update(self, obj_id: str, data: Dict[str, Any]) -> Optional[T]:
        """Update an object."""
        pass
    
    @abstractmethod
    def delete(self, obj_id: str) -> bool:
        """Delete an object."""
        pass
    
    @abstractmethod
    def filter_by(self, **kwargs) -> List[T]:
        """Filter objects by criteria."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Count all objects."""
        pass
    
    @abstractmethod
    def exists(self, obj_id: str) -> bool:
        """Check if object exists."""
        pass

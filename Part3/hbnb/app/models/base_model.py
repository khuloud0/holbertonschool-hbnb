#!/usr/bin/python3
"""Base model: id, created_at, updated_at, save, update."""

import uuid
from datetime import datetime
from typing import Any, Dict


class BaseModel:
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        now = datetime.utcnow()
        self.created_at = now
        self.updated_at = now

    def save(self) -> None:
        """Refresh updated_at."""
        self.updated_at = datetime.utcnow()

    def update(self, data: Dict[str, Any]) -> None:
        """Update attributes then call save()."""
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")

        protected = {"id", "created_at", "updated_at"}
        for key, value in data.items():
            if key in protected:
                continue
            if hasattr(self, key):
                setattr(self, key, value)

        self.save()

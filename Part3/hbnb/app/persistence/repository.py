#!/usr/bin/python3
"""In-memory repository with CRUD + User email uniqueness."""

from typing import Dict, Any, List


class InMemoryRepository:
    def __init__(self):
        # Structure: { "ClassName": { "id": object } }
        self._data: Dict[str, Dict[str, Any]] = {}

    def add(self, obj) -> Any:
        cls = obj.__class__.__name__
        self._data.setdefault(cls, {})

        # Enforce email uniqueness for User
        if cls == "User":
            email = getattr(obj, "email", None)
            if email is None:
                raise ValueError("email is required")

            for existing in self._data[cls].values():
                if existing.email == email:
                    raise ValueError("email must be unique")

        # STORE the object (this was missing in your snippet)
        self._data[cls][obj.id] = obj
        return obj

    def get(self, cls_name: str, obj_id: str):
        return self._data.get(cls_name, {}).get(obj_id)

    def all(self, cls_name: str) -> List[Any]:
        return list(self._data.get(cls_name, {}).values())

    def find_user_by_email(self, email: str):
        email = email.strip().lower()
        for user in self._data.get("User", {}).values():
            if user.email == email:
                return user
        return None

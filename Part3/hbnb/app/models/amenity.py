#!/usr/bin/python3
"""Amenity model with validations and admin support."""

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.models.base_model import BaseModel
from flask import current_app


class Amenity(BaseModel):
    def __init__(self, name: str, description: str = "", icon: str = ""):
        super().__init__()
        self.name = self._required_str(name, "name", 50)
        self.description = description if isinstance(description, str) else ""
        self.icon = icon if isinstance(icon, str) else ""
        
        # TASK 4: Track which admin created/modified this amenity
        self.created_by = None  # Will be set by admin when creating
        self.last_modified_by = None

    @staticmethod
    def _required_str(value: str, field: str, max_len: int) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{field} must be a string")
        cleaned = value.strip()
        if cleaned == "":
            raise ValueError(f"{field} is required")
        if len(cleaned) > max_len:
            raise ValueError(f"{field} must be at most {max_len} characters")
        return cleaned

    # ========== TASK 3: PUBLIC ACCESS METHODS ==========
    
    def to_public_dict(self) -> Dict[str, Any]:
        """
        Public representation (for all users).
        TASK 3: Public endpoints should return this
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            'updated_at': self.updated_at.isoformat() if hasattr(self, 'updated_at') else None
        }

    def to_summary_dict(self) -> Dict[str, Any]:
        """
        Summary representation for listings.
        TASK 3: Used in place details for authenticated users
        """
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon
        }

    # ========== TASK 4: ADMIN SUPPORT METHODS ==========
    
    def set_creation_info(self, admin_user) -> None:
        """
        TASK 4: Set admin who created this amenity.
        Called when admin creates a new amenity.
        """
        if hasattr(admin_user, 'id'):
            self.created_by = admin_user.id
            self.last_modified_by = admin_user.id

    def set_modification_info(self, admin_user) -> None:
        """
        TASK 4: Set admin who last modified this amenity.
        Called when admin updates an amenity.
        """
        if hasattr(admin_user, 'id'):
            self.last_modified_by = admin_user.id

    def can_be_modified_by(self, user) -> bool:
        """
        TASK 4: Check if user can modify this amenity.
        Only admins can modify amenities.
        """
        return hasattr(user, 'is_admin') and user.is_admin

    def admin_create(self, admin_user, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        TASK 4: Admin-specific creation method.
        Validates data and sets admin info.
        """
        if not self.can_be_modified_by(admin_user):
            return {'success': False, 'error': 'Admin access required'}
        
        errors = []
        
        # Validate name uniqueness
        if 'name' in data:
            from app import db
            existing_amenity = next(
                (a for a in db.amenities.values() 
                 if a.name.lower() == data['name'].lower().strip()),
                None
            )
            if existing_amenity:
                errors.append(f"Amenity with name '{data['name']}' already exists")
        
        if errors:
            return {'success': False, 'errors': errors}
        
        # Set admin info
        self.set_creation_info(admin_user)
        
        return {'success': True, 'amenity': self}

    def admin_update(self, admin_user, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        TASK 4: Admin-specific update method.
        Allows admins to update any amenity.
        """
        if not self.can_be_modified_by(admin_user):
            return {'success': False, 'error': 'Admin access required'}
        
        updates = {}
        errors = []
        
        # Name update with uniqueness check
        if 'name' in data:
            try:
                new_name = self._required_str(data['name'], "name", 50)
                
                # Check for duplicate name (excluding current amenity)
                from app import db
                existing_amenity = next(
                    (a for a in db.amenities.values() 
                     if a.id != self.id and 
                     a.name.lower() == new_name.lower()),
                    None
                )
                
                if existing_amenity:
                    errors.append(f"Amenity with name '{new_name}' already exists")
                else:
                    updates['name'] = new_name
                    
            except (TypeError, ValueError) as e:
                errors.append(str(e))
        
        # Description update
        if 'description' in data:
            if isinstance(data['description'], str):
                updates['description'] = data['description']
            else:
                errors.append("description must be a string")
        
        # Icon update
        if 'icon' in data:
            if isinstance(data['icon'], str):
                updates['icon'] = data['icon']
            else:
                errors.append("icon must be a string")
        
        if errors:
            return {'success': False, 'errors': errors}
        
        # Apply updates
        for key, value in updates.items():
            setattr(self, key, value)
        
        # Set modification info
        self.set_modification_info(admin_user)
        
        # Update timestamp
        self.updated_at = datetime.utcnow()
        
        return {'success': True, 'amenity': self.to_admin_dict(admin_user)}

    def admin_delete(self, admin_user) -> Dict[str, Any]:
        """
        TASK 4: Admin-specific delete method.
        Admins can delete any amenity with cleanup.
        """
        if not self.can_be_modified_by(admin_user):
            return {'success': False, 'error': 'Admin access required'}
        
        try:
            from app import db
            
            # Remove from all places that have this amenity
            for place in db.places.values():
                if hasattr(place, 'amenities') and self in place.amenities:
                    place.amenities.remove(self)
            
            # Delete from storage
            db.amenities.pop(self.id, None)
            
            return {
                'success': True, 
                'message': f'Amenity "{self.name}" deleted by admin',
                'deleted_by': admin_user.id if hasattr(admin_user, 'id') else None
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def to_admin_dict(self, requesting_admin) -> Dict[str, Any]:
        """
        TASK 4: Admin-only representation with audit info.
        Includes who created and last modified the amenity.
        """
        from app import db
        
        data = self.to_public_dict()
        
        # Add admin audit info
        data['audit_info'] = {
            'created_by': self.created_by,
            'created_by_email': None,
            'last_modified_by': self.last_modified_by,
            'last_modified_by_email': None
        }
        
        # Resolve admin emails if available
        if self.created_by:
            creator = db.users_by_id.get(self.created_by)
            if creator and hasattr(creator, 'email'):
                data['audit_info']['created_by_email'] = creator.email
        
        if self.last_modified_by:
            modifier = db.users_by_id.get(self.last_modified_by)
            if modifier and hasattr(modifier, 'email'):
                data['audit_info']['last_modified_by_email'] = modifier.email
        
        # Add permissions info
        data['permissions'] = {
            'can_edit': self.can_be_modified_by(requesting_admin),
            'can_delete': self.can_be_modified_by(requesting_admin)
        }
        
        return data

    # ========== UTILITY METHODS FOR BOTH TASKS ==========
    
    def get_usage_count(self) -> int:
        """Get number of places using this amenity."""
        from app import db
        
        if not hasattr(db, 'places'):
            return 0
            
        count = 0
        for place in db.places.values():
            if hasattr(place, 'amenities') and self in place.amenities:
                count += 1
        
        return count

    def get_places_using(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get places using this amenity."""
        from app import db
        
        places = []
        for place in db.places.values():
            if hasattr(place, 'amenities') and self in place.amenities:
                places.append({
                    'id': place.id,
                    'title': place.title if hasattr(place, 'title') else 'Unknown',
                    'owner': place.owner.email if hasattr(place, 'owner') and hasattr(place.owner, 'email') else 'Unknown'
                })
                
                if len(places) >= limit:
                    break
        
        return places

    def is_in_use(self) -> bool:
        """Check if any place is using this amenity."""
        return self.get_usage_count() > 0

    def validate_for_assignment(self, place) -> Dict[str, Any]:
        """
        Validate if amenity can be assigned to a place.
        Can add business rules here (e.g., maximum amenities per place)
        """
        # Example: Check if place already has this amenity
        if hasattr(place, 'amenities') and self in place.amenities:
            return {
                'valid': False,
                'error': f'Place already has amenity "{self.name}"'
            }
        
        # Example: Check maximum amenities limit
        if hasattr(place, 'amenities') and len(place.amenities) >= 20:
            return {
                'valid': False,
                'error': 'Maximum amenities limit reached (20)'
            }
        
        return {'valid': True}

    @classmethod
    def search_by_name(cls, search_term: str, exact: bool = False) -> List["Amenity"]:
        """Search amenities by name."""
        from app import db
        
        if not hasattr(db, 'amenities'):
            return []
        
        search_term = search_term.lower().strip()
        
        if exact:
            return [a for a in db.amenities.values() 
                   if a.name.lower() == search_term]
        else:
            return [a for a in db.amenities.values() 
                   if search_term in a.name.lower()]

    @classmethod
    def get_popular(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular amenities by usage."""
        from app import db
        
        if not hasattr(db, 'amenities'):
            return []
        
        amenities_with_usage = []
        for amenity in db.amenities.values():
            usage_count = amenity.get_usage_count()
            amenities_with_usage.append({
                'amenity': amenity,
                'usage_count': usage_count
            })
        
        # Sort by usage count descending
        amenities_with_usage.sort(key=lambda x: x['usage_count'], reverse=True)
        
        # Return limited results
        return [
            {
                'id': item['amenity'].id,
                'name': item['amenity'].name,
                'usage_count': item['usage_count'],
                'places': item['amenity'].get_places_using(3)
            }
            for item in amenities_with_usage[:limit]
        ]

    def serialize_for_api(self, include_audit: bool = False) -> Dict[str, Any]:
        """
        Serialize amenity for API response.
        TASK 3 & 4: Different levels of detail based on authentication
        """
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'usage_count': self.get_usage_count(),
            'is_in_use': self.is_in_use(),
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            'updated_at': self.updated_at.isoformat() if hasattr(self, 'updated_at') else None
        }
        
        if include_audit:
            data['audit'] = {
                'created_by': self.created_by,
                'last_modified_by': self.last_modified_by
            }
            data['permissions'] = {
                'can_edit': True,  # Assuming admin since include_audit is True
                'can_delete': not self.is_in_use()  # Don't allow delete if in use
            }
        
        return data

    def __repr__(self) -> str:
        """String representation."""
        usage = self.get_usage_count()
        return f"<Amenity {self.id}: {self.name} (Used by {usage} places)>"

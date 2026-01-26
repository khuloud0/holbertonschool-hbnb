#!/usr/bin/python3
"""Place model with validations, relationships, and methods."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from flask import current_app


class Place(BaseModel):
    def __init__(
        self,
        title: str,
        owner: User,
        description: str = "",
        price: float = 1.0,
        latitude: float = 0.0,
        longitude: float = 0.0
    ):
        super().__init__()
        self.title = self._required_str(title, "title", 100)
        self.description = description if isinstance(description, str) else ""
        self.price = self._positive_float(price, "price")
        self.latitude = self._range_float(latitude, "latitude", -90.0, 90.0)
        self.longitude = self._range_float(longitude, "longitude", -180.0, 180.0)
        self.owner = self._owner(owner)
        
        # TASK 3: Add user_id for authentication checks
        self.user_id = owner.id

        # required relationship containers
        self.reviews: List["Review"] = []
        self.amenities: List[Amenity] = []

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

    @staticmethod
    def _positive_float(value, field: str) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{field} must be a float")
        val = float(value)
        if val <= 0:
            raise ValueError(f"{field} must be positive")
        return val

    @staticmethod
    def _range_float(value, field: str, min_v: float, max_v: float) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{field} must be a float")
        val = float(value)
        if val < min_v or val > max_v:
            raise ValueError(f"{field} must be between {min_v} and {max_v}")
        return val

    @staticmethod
    def _owner(owner: User) -> User:
        if not isinstance(owner, User):
            raise TypeError("owner must be a User instance")
        return owner

    def add_review(self, review: "Review") -> None:
        from app.models.review import Review  # local import avoids circular import
        if not isinstance(review, Review):
            raise TypeError("review must be a Review instance")
        if review.place is not self:
            raise ValueError("review.place must reference this Place")
        if review in self.reviews:
            return
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity: Amenity) -> None:
        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity instance")
        if amenity in self.amenities:
            return
        self.amenities.append(amenity)
        self.save()

    # ========== TASK 3: AUTHENTICATION SUPPORT METHODS ==========
    
    def can_be_modified_by(self, user: User) -> bool:
        """
        Check if a user can modify this place.
        TASK 3: Only owner can modify (unless admin - handled separately in decorator)
        """
        return user.id == self.user_id

    def can_be_reviewed_by(self, user: User) -> bool:
        """
        Check if a user can review this place.
        TASK 3: Users cannot review their own places
        """
        return user.id != self.user_id

    def has_review_from_user(self, user: User) -> bool:
        """
        Check if user has already reviewed this place.
        TASK 3: Prevent duplicate reviews
        """
        return any(review.user_id == user.id for review in self.reviews)

    def to_public_dict(self) -> Dict[str, Any]:
        """
        Public representation (for unauthenticated users).
        TASK 3: Public endpoints should return this
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            } if self.owner else None,
            'amenities': [amenity.to_dict() for amenity in self.amenities],
            'reviews_count': len(self.reviews),
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            'updated_at': self.updated_at.isoformat() if hasattr(self, 'updated_at') else None
        }

    def to_private_dict(self, requesting_user: Optional[User] = None) -> Dict[str, Any]:
        """
        Private representation (for authenticated users or owners).
        TASK 3: Includes more details for authorized users
        """
        data = self.to_public_dict()
        
        # Add owner contact info only if user owns the place or is admin
        if requesting_user and (requesting_user.id == self.user_id or requesting_user.is_admin):
            data['owner_details'] = {
                'full_contact': f"{self.owner.first_name} {self.owner.last_name}",
                'email': self.owner.email
            }
        
        # Add reviews if user is owner or admin
        if requesting_user and (requesting_user.id == self.user_id or requesting_user.is_admin):
            from app.models.review import Review
            data['reviews'] = [review.to_dict() for review in self.reviews]
        
        return data

    # ========== TASK 4: ADMIN SUPPORT METHODS ==========
    
    def can_be_accessed_by_admin(self, admin_user: User) -> bool:
        """
        TASK 4: Check if admin can access/modify this place.
        Admins can access any place regardless of ownership.
        """
        return admin_user.is_admin if hasattr(admin_user, 'is_admin') else False

    def admin_update(self, data: Dict[str, Any], admin_user: User) -> Dict[str, Any]:
        """
        TASK 4: Admin-specific update method.
        Allows admins to update any field, including transferring ownership.
        """
        if not self.can_be_accessed_by_admin(admin_user):
            return {'success': False, 'error': 'Admin access required'}
        
        updates = {}
        errors = []
        
        # Title update
        if 'title' in data:
            try:
                updates['title'] = self._required_str(data['title'], "title", 100)
            except (TypeError, ValueError) as e:
                errors.append(str(e))
        
        # Description update
        if 'description' in data:
            if isinstance(data['description'], str):
                updates['description'] = data['description']
            else:
                errors.append("description must be a string")
        
        # Price update
        if 'price' in data:
            try:
                updates['price'] = self._positive_float(data['price'], "price")
            except (TypeError, ValueError) as e:
                errors.append(str(e))
        
        # Location updates
        if 'latitude' in data:
            try:
                updates['latitude'] = self._range_float(data['latitude'], "latitude", -90.0, 90.0)
            except (TypeError, ValueError) as e:
                errors.append(str(e))
        
        if 'longitude' in data:
            try:
                updates['longitude'] = self._range_float(data['longitude'], "longitude", -180.0, 180.0)
            except (TypeError, ValueError) as e:
                errors.append(str(e))
        
        # TASK 4: Admin can change owner
        if 'owner_id' in data:
            from app import db
            new_owner = db.users_by_id.get(data['owner_id'])
            if new_owner:
                updates['owner'] = new_owner
                updates['user_id'] = new_owner.id
            else:
                errors.append(f"User with id {data['owner_id']} not found")
        
        if errors:
            return {'success': False, 'errors': errors}
        
        # Apply updates
        for key, value in updates.items():
            setattr(self, key, value)
        
        # Update timestamp
        self.updated_at = datetime.utcnow()
        
        return {'success': True, 'place': self.to_private_dict(admin_user)}

    def admin_delete(self, admin_user: User) -> Dict[str, Any]:
        """
        TASK 4: Admin-specific delete method.
        Admins can delete any place.
        """
        if not self.can_be_accessed_by_admin(admin_user):
            return {'success': False, 'error': 'Admin access required'}
        
        try:
            # Delete associated reviews
            from app import db
            review_ids_to_delete = [
                rid for rid, review in db.reviews.items() 
                if str(review.place_id) == str(self.id)
            ]
            
            for rid in review_ids_to_delete:
                db.reviews.pop(rid, None)
            
            # Delete from storage
            db.places.pop(self.id, None)
            
            return {'success': True, 'message': 'Place deleted by admin'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    # ========== UTILITY METHODS FOR BOTH TASKS ==========
    
    def get_average_rating(self) -> Optional[float]:
        """Calculate average rating from reviews."""
        if not self.reviews:
            return None
        
        total = sum(review.rating for review in self.reviews)
        return round(total / len(self.reviews), 1)

    def get_reviews_by_user(self, user: User) -> List["Review"]:
        """Get all reviews by a specific user for this place."""
        return [review for review in self.reviews if review.user_id == user.id]

    def remove_amenity(self, amenity: Amenity) -> None:
        """Remove an amenity from the place."""
        if amenity in self.amenities:
            self.amenities.remove(amenity)
            self.save()

    def clear_amenities(self) -> None:
        """Remove all amenities from the place."""
        self.amenities.clear()
        self.save()

    def validate_for_creation(self, user: User) -> Dict[str, Any]:
        """
        Validate if place can be created by user.
        TASK 3: Check if user is authenticated
        """
        if not user or not hasattr(user, 'id'):
            return {'valid': False, 'error': 'User authentication required'}
        
        # Additional business rules can be added here
        return {'valid': True, 'user_id': user.id}

    @classmethod
    def find_by_owner(cls, owner_id: str) -> List["Place"]:
        """Find all places owned by a specific user."""
        from app import db
        return [place for place in db.places.values() if str(place.user_id) == str(owner_id)]

    @classmethod
    def find_by_amenity(cls, amenity_id: str) -> List["Place"]:
        """Find all places with a specific amenity."""
        from app import db
        return [place for place in db.places.values() 
                if any(str(amenity.id) == str(amenity_id) for amenity in place.amenities)]

    def serialize_for_api(self, include_owner_details: bool = False) -> Dict[str, Any]:
        """
        Serialize place for API response.
        TASK 3 & 4: Different levels of detail based on authentication
        """
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'location': {
                'latitude': self.latitude,
                'longitude': self.longitude
            },
            'owner_id': self.user_id,
            'amenity_ids': [amenity.id for amenity in self.amenities],
            'review_ids': [review.id for review in self.reviews],
            'average_rating': self.get_average_rating(),
            'total_reviews': len(self.reviews),
            'total_amenities': len(self.amenities),
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            'updated_at': self.updated_at.isoformat() if hasattr(self, 'updated_at') else None
        }
        
        if include_owner_details and self.owner:
            data['owner'] = {
                'id': self.owner.id,
                'name': f"{self.owner.first_name} {self.owner.last_name}",
                'email': self.owner.email
            }
        
        return data

    def __repr__(self) -> str:
        """String representation."""
        return f"<Place {self.id}: {self.title} (Owner: {self.owner.email if self.owner else 'None'})>"

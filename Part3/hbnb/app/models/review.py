#!/usr/bin/python3
"""Review model with validations and references."""

from typing import Dict, Any, Optional
from datetime import datetime
from app.models.base_model import BaseModel
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text: str, rating: int, user: User, place):
        super().__init__()
        self.text = self._required_text(text)
        self.rating = self._rating(rating)
        self.user = self._user(user)
        self.place = self._place(place)
        
        # TASK 3: Add IDs for authentication checks
        self.user_id = user.id
        self.place_id = place.id

    @staticmethod
    def _required_text(value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("text must be a string")
        cleaned = value.strip()
        if cleaned == "":
            raise ValueError("text is required")
        return cleaned

    @staticmethod
    def _rating(value: int) -> int:
        if not isinstance(value, int):
            raise TypeError("rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("rating must be between 1 and 5")
        return value

    @staticmethod
    def _user(user: User) -> User:
        if not isinstance(user, User):
            raise TypeError("user must be a User instance")
        return user

    @staticmethod
    def _place(place):
        from app.models.place import Place  # local import avoids circular import
        if not isinstance(place, Place):
            raise TypeError("place must be a Place instance")
        return place

    # ========== TASK 3: AUTHENTICATION SUPPORT METHODS ==========
    
    def can_be_modified_by(self, user: User) -> bool:
        """
        Check if a user can modify this review.
        TASK 3: Only the author can modify their review
        """
        return user.id == self.user_id

    def can_be_created_by(self, user: User) -> Dict[str, Any]:
        """
        Validate if user can create this review.
        TASK 3: Users cannot review their own places and cannot review same place twice
        """
        from app import db
        
        # Check if user owns the place
        if str(user.id) == str(self.place.user_id):
            return {
                'allowed': False,
                'error': 'You cannot review your own place'
            }
        
        # Check for existing review by same user for same place
        existing_review = next(
            (r for r in db.reviews.values() 
             if str(r.user_id) == str(user.id) and str(r.place_id) == str(self.place_id)),
            None
        )
        
        if existing_review:
            return {
                'allowed': False,
                'error': 'You have already reviewed this place'
            }
        
        return {'allowed': True}

    def to_public_dict(self) -> Dict[str, Any]:
        """
        Public representation (for unauthenticated users).
        TASK 3: Public endpoints should return this
        """
        return {
            'id': self.id,
            'text': self.text[:100] + "..." if len(self.text) > 100 else self.text,  # Preview
            'rating': self.rating,
            'user': {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name
            } if self.user else None,
            'place': {
                'id': self.place.id,
                'title': self.place.title
            } if self.place else None,
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            'updated_at': self.updated_at.isoformat() if hasattr(self, 'updated_at') else None
        }

    def to_private_dict(self, requesting_user: Optional[User] = None) -> Dict[str, Any]:
        """
        Private representation (for authenticated users).
        TASK 3: Includes full text for authorized users
        """
        data = self.to_public_dict()
        
        # Replace preview with full text for authenticated users
        data['text'] = self.text
        
        # Add more details if user is the author or admin
        if requesting_user and (requesting_user.id == self.user_id or 
                               (hasattr(requesting_user, 'is_admin') and requesting_user.is_admin)):
            data['user_details'] = {
                'email': self.user.email if self.user else None
            }
            data['can_edit'] = True
            data['can_delete'] = True
        
        return data

    # ========== TASK 4: ADMIN SUPPORT METHODS ==========
    
    def can_be_accessed_by_admin(self, admin_user: User) -> bool:
        """
        TASK 4: Check if admin can access/modify this review.
        Admins can access any review regardless of authorship.
        """
        return admin_user.is_admin if hasattr(admin_user, 'is_admin') else False

    def admin_update(self, data: Dict[str, Any], admin_user: User) -> Dict[str, Any]:
        """
        TASK 4: Admin-specific update method.
        Allows admins to update any field, including transferring authorship.
        """
        if not self.can_be_accessed_by_admin(admin_user):
            return {'success': False, 'error': 'Admin access required'}
        
        updates = {}
        errors = []
        
        # Text update
        if 'text' in data:
            try:
                updates['text'] = self._required_text(data['text'])
            except (TypeError, ValueError) as e:
                errors.append(str(e))
        
        # Rating update
        if 'rating' in data:
            try:
                updates['rating'] = self._rating(int(data['rating']))
            except (TypeError, ValueError) as e:
                errors.append(str(e))
        
        # TASK 4: Admin can change author
        if 'user_id' in data:
            from app import db
            new_user = db.users_by_id.get(data['user_id'])
            if new_user:
                updates['user'] = new_user
                updates['user_id'] = new_user.id
                
                # Check if new user can review this place
                validation = self.can_be_created_by(new_user)
                if not validation['allowed']:
                    errors.append(f"Cannot assign to new user: {validation['error']}")
            else:
                errors.append(f"User with id {data['user_id']} not found")
        
        # TASK 4: Admin can change place
        if 'place_id' in data:
            from app import db
            new_place = db.places.get(data['place_id'])
            if new_place:
                updates['place'] = new_place
                updates['place_id'] = new_place.id
                
                # Check if user can review new place
                if 'user' not in updates:  # If user not being changed
                    validation = self.can_be_created_by(self.user)
                    if not validation['allowed']:
                        errors.append(f"Cannot assign to new place: {validation['error']}")
            else:
                errors.append(f"Place with id {data['place_id']} not found")
        
        if errors:
            return {'success': False, 'errors': errors}
        
        # Apply updates
        for key, value in updates.items():
            setattr(self, key, value)
        
        # Update timestamp
        self.updated_at = datetime.utcnow()
        
        return {'success': True, 'review': self.to_private_dict(admin_user)}

    def admin_delete(self, admin_user: User) -> Dict[str, Any]:
        """
        TASK 4: Admin-specific delete method.
        Admins can delete any review.
        """
        if not self.can_be_accessed_by_admin(admin_user):
            return {'success': False, 'error': 'Admin access required'}
        
        try:
            from app import db
            
            # Remove from storage
            db.reviews.pop(self.id, None)
            
            # Remove from place's reviews list
            if self.place and hasattr(self.place, 'reviews') and self in self.place.reviews:
                self.place.reviews.remove(self)
            
            return {'success': True, 'message': 'Review deleted by admin'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    # ========== UTILITY METHODS FOR BOTH TASKS ==========
    
    def get_star_rating(self) -> str:
        """Convert numeric rating to star representation."""
        return "★" * self.rating + "☆" * (5 - self.rating)

    def is_positive(self, threshold: int = 3) -> bool:
        """Check if review is positive based on threshold."""
        return self.rating >= threshold

    def truncate_text(self, max_length: int = 200) -> str:
        """Truncate text for preview purposes."""
        if len(self.text) <= max_length:
            return self.text
        return self.text[:max_length] + "..."

    @classmethod
    def find_by_user(cls, user_id: str) -> list["Review"]:
        """Find all reviews by a specific user."""
        from app import db
        return [review for review in db.reviews.values() if str(review.user_id) == str(user_id)]

    @classmethod
    def find_by_place(cls, place_id: str) -> list["Review"]:
        """Find all reviews for a specific place."""
        from app import db
        return [review for review in db.reviews.values() if str(review.place_id) == str(place_id)]

    @classmethod
    def find_by_rating(cls, min_rating: int = 1, max_rating: int = 5) -> list["Review"]:
        """Find reviews within a rating range."""
        from app import db
        return [review for review in db.reviews.values() 
                if min_rating <= review.rating <= max_rating]

    def validate_for_update(self, user: User, new_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate if review can be updated by user.
        TASK 3: Check permissions and validate new data
        """
        if not user:
            return {'valid': False, 'error': 'User authentication required'}
        
        # Check if user is the author (unless admin)
        if user.id != self.user_id and not (hasattr(user, 'is_admin') and user.is_admin):
            return {'valid': False, 'error': 'You can only edit your own reviews'}
        
        # Validate new text if provided
        if 'text' in new_data:
            try:
                self._required_text(new_data['text'])
            except (TypeError, ValueError) as e:
                return {'valid': False, 'error': str(e)}
        
        # Validate new rating if provided
        if 'rating' in new_data:
            try:
                self._rating(int(new_data['rating']))
            except (TypeError, ValueError) as e:
                return {'valid': False, 'error': str(e)}
        
        return {'valid': True}

    def serialize_for_api(self, include_user_details: bool = False, 
                         include_place_details: bool = False) -> Dict[str, Any]:
        """
        Serialize review for API response.
        TASK 3 & 4: Different levels of detail based on authentication
        """
        data = {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'star_rating': self.get_star_rating(),
            'is_positive': self.is_positive(),
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            'updated_at': self.updated_at.isoformat() if hasattr(self, 'updated_at') else None
        }
        
        if include_user_details and self.user:
            data['user'] = {
                'id': self.user.id,
                'name': f"{self.user.first_name} {self.user.last_name}",
                'email': self.user.email if hasattr(self.user, 'email') else None
            }
        
        if include_place_details and self.place:
            data['place'] = {
                'id': self.place.id,
                'title': self.place.title,
                'price': self.place.price if hasattr(self.place, 'price') else None
            }
        
        return data

    def copy_to_new_place(self, new_place, new_user: Optional[User] = None) -> "Review":
        """
        Create a copy of this review for a new place.
        Useful for admin operations.
        """
        from app.models.review import Review
        
        user_to_use = new_user if new_user else self.user
        new_review = Review(
            text=self.text,
            rating=self.rating,
            user=user_to_use,
            place=new_place
        )
        
        return new_review

    def __repr__(self) -> str:
        """String representation."""
        place_title = self.place.title if self.place else 'Unknown Place'
        user_name = f"{self.user.first_name} {self.user.last_name}" if self.user else 'Unknown User'
        return f"<Review {self.id}: {self.rating}★ for '{place_title}' by {user_name}>"

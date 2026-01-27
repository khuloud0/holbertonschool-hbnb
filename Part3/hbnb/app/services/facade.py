#!/usr/bin/python3
"""Facade service updated to use SQLAlchemyRepository."""

from typing import Optional, List, Dict, Any
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """Main service facade with SQLAlchemy repository."""
    
    def __init__(self):
        # Initialize SQLAlchemy repositories
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
    
    # User operations
    def create_user(self, first_name: str, last_name: str, email: str, 
                   password: str, is_admin: bool = False) -> Optional[User]:
        """Create a new user."""
        try:
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_admin=is_admin
            )
            return self.user_repo.create(user)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.user_repo.get_by(email=email)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user."""
        user = self.get_user_by_email(email)
        if user and user.check_password(password):
            return user
        return None
    
    def update_user(self, user_id: str, data: Dict[str, Any]) -> Optional[User]:
        """Update user."""
        return self.user_repo.update(user_id, data)
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user."""
        return self.user_repo.delete(user_id)
    
    # Place operations
    def create_place(self, title: str, owner: User, description: str = "",
                    price: float = 1.0, latitude: float = 0.0, 
                    longitude: float = 0.0) -> Optional[Place]:
        """Create a new place."""
        try:
            place = Place(
                title=title,
                owner=owner,
                description=description,
                price=price,
                latitude=latitude,
                longitude=longitude
            )
            return self.place_repo.create(place)
        except Exception as e:
            print(f"Error creating place: {e}")
            return None
    
    def get_place(self, place_id: str) -> Optional[Place]:
        """Get place by ID."""
        return self.place_repo.get(place_id)
    
    def get_places_by_owner(self, owner_id: str) -> List[Place]:
        """Get places by owner."""
        return self.place_repo.filter_by(user_id=owner_id)
    
    def update_place(self, place_id: str, data: Dict[str, Any]) -> Optional[Place]:
        """Update place."""
        return self.place_repo.update(place_id, data)
    
    def delete_place(self, place_id: str) -> bool:
        """Delete place."""
        return self.place_repo.delete(place_id)
    
    # Review operations
    def create_review(self, text: str, rating: int, user: User, 
                     place: Place) -> Optional[Review]:
        """Create a new review."""
        try:
            # Check if user can review this place
            if place.user_id == user.id:
                print("User cannot review their own place")
                return None
            
            # Check for duplicate review
            existing = self.review_repo.filter_by(
                user_id=user.id,
                place_id=place.id
            )
            if existing:
                print("User has already reviewed this place")
                return None
            
            review = Review(
                text=text,
                rating=rating,
                user=user,
                place=place
            )
            return self.review_repo.create(review)
        except Exception as e:
            print(f"Error creating review: {e}")
            return None
    
    def get_review(self, review_id: str) -> Optional[Review]:
        """Get review by ID."""
        return self.review_repo.get(review_id)
    
    def get_reviews_by_place(self, place_id: str) -> List[Review]:
        """Get reviews for a place."""
        return self.review_repo.filter_by(place_id=place_id)
    
    def get_reviews_by_user(self, user_id: str) -> List[Review]:
        """Get reviews by a user."""
        return self.review_repo.filter_by(user_id=user_id)
    
    def update_review(self, review_id: str, data: Dict[str, Any]) -> Optional[Review]:
        """Update review."""
        return self.review_repo.update(review_id, data)
    
    def delete_review(self, review_id: str) -> bool:
        """Delete review."""
        return self.review_repo.delete(review_id)
    
    # Amenity operations
    def create_amenity(self, name: str) -> Optional[Amenity]:
        """Create a new amenity."""
        try:
            amenity = Amenity(name=name)
            return self.amenity_repo.create(amenity)
        except Exception as e:
            print(f"Error creating amenity: {e}")
            return None
    
    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        """Get amenity by ID."""
        return self.amenity_repo.get(amenity_id)
    
    def get_amenity_by_name(self, name: str) -> Optional[Amenity]:
        """Get amenity by name."""
        return self.amenity_repo.get_by(name=name)
    
    def update_amenity(self, amenity_id: str, data: Dict[str, Any]) -> Optional[Amenity]:
        """Update amenity."""
        return self.amenity_repo.update(amenity_id, data)
    
    def delete_amenity(self, amenity_id: str) -> bool:
        """Delete amenity."""
        return self.amenity_repo.delete(amenity_id)
    
    # Statistics and utility methods
    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get statistics for a user."""
        user = self.get_user(user_id)
        if not user:
            return {}
        
        places = self.get_places_by_owner(user_id)
        reviews = self.get_reviews_by_user(user_id)
        
        return {
            'user': user.to_dict(),
            'places_count': len(places),
            'reviews_count': len(reviews),
            'places': [p.to_dict() for p in places[:5]],
            'reviews': [r.to_dict() for r in reviews[:5]]
        }
    
    def get_place_statistics(self, place_id: str) -> Dict[str, Any]:
        """Get statistics for a place."""
        place = self.get_place(place_id)
        if not place:
            return {}
        
        reviews = self.get_reviews_by_place(place_id)
        avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
        
        return {
            'place': place.to_dict(),
            'reviews_count': len(reviews),
            'average_rating': round(avg_rating, 1),
            'reviews': [r.to_dict() for r in reviews[:5]]
        }
    
    def search_places(self, query: str, **filters) -> List[Place]:
        """Search places with filters."""
        all_places = self.place_repo.get_all()
        results = []
        
        for place in all_places:
            # Text search in title and description
            if query and query.lower() not in place.title.lower() and \
               query.lower() not in place.description.lower():
                continue
            
            # Apply filters
            match = True
            for key, value in filters.items():
                if hasattr(place, key) and getattr(place, key) != value:
                    match = False
                    break
            
            if match:
                results.append(place)
        
        return results

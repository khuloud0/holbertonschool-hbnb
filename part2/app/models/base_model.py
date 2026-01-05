import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        self.updated_at = datetime.utcnow()

  @classmethod
    def from_dict(cls, data: dict):
        """Create an instance from a dictionary (factory method)"""
        # Create instance without calling __init__ to avoid double ID generation
        instance = cls.__new__(cls)
        
        # Set attributes from dictionary
        for key, value in data.items():
            # Convert string dates back to datetime objects
            if key in ['created_at', 'updated_at'] and isinstance(value, str):
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    # Fallback for other date formats if needed
                    pass
            setattr(instance, key, value)
        
        return instance
    
    def __str__(self):
        """String representation of the object"""
        class_name = self.__class__.__name__
        attrs = {}
        
        # Get all non-callable attributes that don't start with underscore
        for key in dir(self):
            if not key.startswith('_') and not callable(getattr(self, key)):
                attrs[key] = getattr(self, key)
        
        return f"[{class_name}] ({self.id}) {attrs}"
    
    def __repr__(self):
        """Official string representation"""
        return self.__str__()

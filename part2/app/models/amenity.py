from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name: str, description: str = ""):
        super().__init__()
        self.name = name
        self.description = description

  def to_dict(self):
        """Convert object to dictionary"""
        base_dict = super().to_dict() if hasattr(super(), 'to_dict') else {}
        return {
            **base_dict,
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    
    def update(self, data: dict):
        """Update amenity data"""
        if 'name' in data:
            self.name = data['name']
        if 'description' in data:
            self.description = data['description']
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create object from dictionary"""
        return cls(
            name=data.get('name', ''),
            description=data.get('description', '')
        )

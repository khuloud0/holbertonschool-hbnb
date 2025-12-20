# High-Level Package Diagram

![High-Level Package Diagram](high_level_package_diagram.svg)

## Explanation
The application follows a three-layer architecture.
The Presentation Layer handles API requests and user interaction.
The Business Logic Layer contains the core models and application logic.
The Persistence Layer manages data storage and retrieval.
Communication between layers is handled using the Facade Pattern to ensure separation of concerns.

```mermaid
classDiagram

class PresentationLayer {
  <<Interface>>
  +API
  +Services
}

class BusinessLogicLayer {
  +User
  +Place
  +Review
  +Amenity
}

class PersistenceLayer {
  +Database
  +Repositories
}

PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Data Access

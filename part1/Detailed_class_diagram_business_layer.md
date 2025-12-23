# Detailed Class Diagram for Business Logic Layer

## Overview

This document presents a detailed class diagram for the **Business Logic Layer** of the HBNB application.
It illustrates the core business entities, their attributes, methods, and the relationships between them.
The goal is to clearly define responsibilities and interactions before implementation.

The main entities covered in this layer are:
- User
- Place
- Review
- Amenity

---

## Core Entities

### User

Represents a person using the platform.

**Attributes:**
- id: string
- first_name: string
- last_name: string
- email: string
- password: string
- is_admin: boolean
- created_at: datetime
- updated_at: datetime

**Methods:**
- register()
- update()
- delete()

A user can own places and write reviews.  
Some users may have administrative privileges.

---

### Place

Represents a property listed on the platform.

**Attributes:**
- id: string
- title: string
- description: string
- price: float
- latitude: float
- longitude: float
- created_at: datetime
- updated_at: datetime

**Methods:**
- create()
- update()
- delete()
- list()

Each place belongs to one user and can include multiple amenities and reviews.

---

### Review

Represents feedback written by a user for a specific place.

**Attributes:**
- id: string
- rating: int
- comment: string
- created_at: datetime
- updated_at: datetime

**Methods:**
- create()
- update()
- delete()
- list_by_place()

Each review is associated with exactly one user and one place.

---

### Amenity

Represents features associated with places, such as Wi-Fi or parking.

**Attributes:**
- id: string
- name: string
- description: string
- created_at: datetime
- updated_at: datetime

**Methods:**
- create()
- update()
- delete()
- list()

Amenities can be shared across multiple places.

---

## Entity Relationships

- A **User** can own **zero or more Places**.
- A **User** can write **multiple Reviews**.
- A **Place** belongs to **one User**.
- A **Place** can have **multiple Reviews**.
- A **Place** can include **multiple Amenities**.
- An **Amenity** can be associated with **multiple Places**.

---

## Detailed Class Diagram

The following diagram visually represents the entities, their attributes, methods,
and relationships within the Business Logic Layer.

![Detailed Class Diagram](Detailed_Class_Diagram_for_Business_Logic_Layer.svg)

---

## Conclusion

This detailed class diagram ensures that the business logic of the HBNB application
is well-structured and clearly defined.  
By separating responsibilities and defining clear relationships between entities,
the system becomes easier to maintain, extend, and implement.

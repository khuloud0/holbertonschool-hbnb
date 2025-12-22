# HBNB Technical Documentation

## Introduction
This document provides a comprehensive technical overview of the HBNB application.
It compiles all UML diagrams created in previous tasks into a single, structured
reference document.

The purpose of this documentation is to clearly describe the system architecture,
the business logic layer, and the interaction flow between the user, API, business
logic, and database. This document serves as a blueprint to guide future
implementation phases of the project.

---

## High-Level Architecture

This section presents the high-level package diagram of the HBNB application.

The diagram illustrates the layered architecture used in the system, which is
divided into the following main layers:

- **Presentation Layer (API):** Handles incoming user requests and responses.
- **Business Logic Layer:** Contains the core application logic and validation.
- **Persistence Layer (Database):** Responsible for data storage and retrieval.

This separation of concerns improves maintainability, scalability, and clarity
of the overall system design.

![High Level Package Diagram](High_Level_Package_Diagram.svg)

---

## Business Logic Layer

This section describes the detailed class diagram for the Business Logic Layer
of the HBNB application.

The diagram illustrates the core entities of the system, their attributes,
methods, and the relationships between them. These entities represent the
foundation of the application’s domain model.

### Core Entities

- **User**
  - Represents a person using the platform.
  - A user can register, update their profile, own places, and write reviews.
  - A user may have administrative privileges.

- **Place**
  - Represents a property listed on the platform.
  - Each place belongs to a user and can include multiple amenities and reviews.

- **Review**
  - Represents feedback written by a user for a specific place.
  - Each review is associated with exactly one user and one place.

- **Amenity**
  - Represents features associated with places, such as Wi-Fi or parking.
  - Amenities can be shared across multiple places.

This class diagram ensures that relationships and responsibilities between
entities are clearly defined before implementation.

![Detailed Class Diagram](Detailed_Class_Diagram_for_Business_Logic_Layer.svg)

---

## API Interaction Flow

This section presents sequence diagrams that illustrate how different API calls
are processed within the HBNB application.

Each sequence diagram demonstrates the interaction between:
- The **User**
- The **API layer**
- The **Business Logic layer**
- The **Database**

These diagrams help clarify request handling, data processing, and response flow.

---

### User Registration

This sequence diagram describes the process of user registration.

The flow includes:
1. The user submitting registration data via the API.
2. The API forwarding the request to the Business Logic layer.
3. Validation and processing of the data.
4. Storing the user information in the database.
5. Returning a confirmation response to the user.

![User Registration Sequence](Sequence_Diagram_User_Registration.svg)

---

### Place Creation

This sequence diagram illustrates how a user creates a new place listing.

The flow includes:
1. The user sending place data through the API.
2. Business logic validation and processing.
3. Persisting the place data in the database.
4. Returning a success response to the user.

![Place Creation Sequence](Sequence_Diagram_Place_Creation.svg)

---

### Fetching a List of Places

This sequence diagram explains how the system retrieves a list of available places.

The flow includes:
1. The user requesting a list of places.
2. The API processing the request.
3. The Business Logic layer fetching the data from the database.
4. Returning the list of places to the user.

![Fetch Places List Sequence](Sequence_Diagram_Fetch_Places_List.svg)

---

## Conclusion

This document consolidates all UML diagrams created for the HBNB project into a
single technical reference. It provides a clear understanding of the system’s
architecture, entity relationships, and API interaction flows.

By organizing these diagrams and explanations in one place, this documentation
supports better collaboration, easier maintenance, and smoother implementation
of future development stages.

# Holberton School HBNB – Part 2 🌍

## Overview 🧭

This project is part of the Holberton School curriculum and represents **Part 2 of the HBNB project**.  
The focus of this stage is building a **RESTful API** using **Python, Flask, and Flask-RESTX**, while applying clean architecture principles such as the **Facade pattern** and **Repository pattern**.

The API allows managing users, places, amenities, and reviews using in-memory data storage.

---

## Key Features ✨

- RESTful API architecture
- CRUD operations for all resources
- Input validation and proper HTTP status codes
- Facade pattern to separate business logic
- In-memory repository for data persistence
- Swagger documentation via Flask-RESTX

---
### 📌 Structure Overview

- **api/v1/**  
  Contains REST API endpoints for all resources (Users, Places, Reviews, Amenities)

- **models/**  
  Defines the data models and the shared base model used across the application

- **services/**  
  Handles the application business logic using the Facade pattern

- **persistence/**  
  Manages data storage using an in-memory repository implementation

- **run.py**  
  Entry point for running the Flask application

- **config.py**  
  Application configuration and environment settings

---

## Installation ⚙️
## 1.Clone the repository
```bash
git clone https://github.com/khuloud0/holbertonschool-hbnb.git
```
## 2.Navigate to the Part 2 project directory
```bash
cd holbertonschool-hbnb/part2
```
## 3. Install the required dependencies
```bash
pip install -r requirements.txt
```
## 4. Run the Flask server
```bash
flask run --host=0.0.0.0 --port=80
```

## Usage 🚀
## 1. Run the Flask server
From the part2 directory, run:
```bash
python3 run.py
```
Alternatively, you can run the server using Flask:
```bash
flask run --host=0.0.0.0 --port=80
```
## 2. Access the API
Once the server is running, the API will be available at:
```bash
http://127.0.0.1:5000
```
or (if running on port 80):
```bash
http://localhost
```
## 3. API Documentation (Swagger)
Swagger UI is available at:
```bash
http://127.0.0.1:5000/api/v1/
```
It provides interactive documentation for all endpoints, including:

- Users
- Places
- Reviews
- Amenities
  
  
## Example API Endpoints 🔗
Below are some example API endpoints that can be tested using curl or via Swagger UI.


- List users
```bash
GET /api/v1/users/
```
- Create a user
```bash
POST /api/v1/users/
```
- List place
```bash
GET /api/v1/Place/
```
- Create a place
```bash
GET /api/v1/places/
```
- List reviews
```bash
GET /api/v1/reviews/
```
- Create a review
```bash
POST /api/v1/reviews/
 ```bash
 -  List amenities
```bash
GET /api/v1/amenities/
```bash
- Create an amenity
```bash
POST /api/v1/amenities/
```bash
## Swagger Documentation
Interactive API documentation is available at:
```bash
http://127.0.0.1:5000/api/v1/
```bash

## API Testing 🧪

Creat a User
```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{
  "first_name": "Test",
  "last_name": "User",
  "email": "test@test.com",
  "password": "1234"
}'
```
Expected response (201 Created )
```bash
"id":<generated_id>",
"first_name": "Test",
"last_name": "User",
"email": "test@test.com"
}'
```
## Testing & Validation
Several issues were discovered during testing, mainly related to serialization, update method signatures, and repository behavior, and were resolved iteratively.

This project was manually tested using **Swagger UI** and **curl** to ensure correct API behavior and business logic validation.

The following areas were tested and verified:

### Resource Creation
- Users can be created successfully (201 Created).
- Places can be created with valid owner IDs.
- Reviews can be created only when user and place exist.

### Field Validation and Error Responses
- Creating resources with missing required fields returns **400 Bad Request**.
- Invalid JSON payloads in Swagger return clear validation errors.
- Invalid foreign IDs (e.g., non-existing owner_id or user_id) return **404 Not Found**.

### Serialization Verification
- Place endpoints now return all expected fields (`title`, `description`, `price`, `latitude`, `longitude`, `owner_id`).
- Review endpoints return full details: `text`, `rating`, `user_id`, `place_id` as well as base fields.
- Fixes were implemented in the `to_dict()` methods of Place and Review to include all attributes.

### Update and Delete Behavior
- PUT endpoints update correct fields and respond with **200 OK**.
- DELETE endpoints remove the resource and subsequent GET returns **404 Not Found**.
- A bug in Review update arguments was resolved by standardizing `review.update(**review_data)`.

### Edge Cases
- Attempting to update or delete a non-existing review returns **404 Review not found**.
- Rating values outside the range 1–5 return validation errors.
- Due to the use of an in-memory repository, data is reset on server restart. All update and delete tests were therefore performed within the same runtime session..

All tests were performed manually and verified against the expected behavior defined in the project specifications.

## Notes

- All endpoints were tested manually using curl
- Swagger documentation was used to verify request and response formats
- In-memory repository was used for data persistence during development and testing


  

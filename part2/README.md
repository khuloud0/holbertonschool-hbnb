# Holberton School HBNB – Part 2 🌍

## Overview 🧭

This project is part of the Holberton School curriculum and represents **Part 2 of the HBNB project**.

The main goal of this stage is to design and implement a **RESTful API** using **Python, Flask, and Flask-RESTX**, while applying clean architecture principles such as the **Facade Pattern** and **Repository Pattern**

The API provides full CRUD operations for managing **Users, Places, Amenities, and Reviews**, using an **in-memory data storage** approach.


---

## Key Features ✨

- RESTful API built with Flask and Flask-RESTX
- Full CRUD operations for all resources
- Clear separation of concerns using the Facade pattern
- In-memory repository for data persistence
- Input validation and proper HTTP status codes
- Interactive API documentation using Swagger UI

---
### 📌 Structure Overview

- **api/v1/**  
  Contains all REST API endpoints for Users, Places, Reviews, and Amenities

- **models/**  
  Defines all entity models and the shared BaseModel

- **services/**  
 Handles the business logic layer using the Facade pattern

- **persistence/**  
  Provides an in-memory repository implementation for data storage

- **run.py**  
  Entry point used to start the Flask application

- **config.py**  
  Contains application configuration and environment settings

---

## Installation ⚙️
Follow the steps below to set up and run the project locally.

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
Once the server is running, the API will be accessible through the base URL below.

The project also provides an interactive Swagger UI that allows testing all endpoints directly from the browser.

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
Below are examples of the main API endpoints available in this project.
These endpoints allow managing users, places, reviews, and amenities through standard HTTP methods.


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
 ```
 -  List amenities
```bash
GET /api/v1/amenities/
```
- Create an amenity
```bash
POST /api/v1/amenities/
```

## Swagger Documentation
Interactive API documentation is available at:
```bash
http://127.0.0.1:5000/api/v1/
```

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
This project was thoroughly tested using curl and Swagger UI to validate both successful and failure scenarios.
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
- The application uses in-memory storage for simplicity and testing purposes

  

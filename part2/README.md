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

1. Clone the repository:

```bash
git clone https://github.com/khuloud0/holbertonschool-hbnb.git
```

2. Navigate to the project directory:

```bash
cd holbertonschool-hbnb/part2
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```


## Usage 🚀

1. Run the Flask server:

```bash
python3 run.py
```
2. The API will be available at:

```bash
http://127.0.0.1:5000
```

Example API Endpoints 🔗

🔹 List users
```bash
GET /api/v1/users/
```
🔹 Create a user
```bash
POST /api/v1/users/
```
🔹 List place
```bash
GET /api/v1/Place/
```
🔹 List reviews
```bash
GET /api/v1/reviews/
```
🔹 List amenities
```bash
GET /api/v1/amenities/
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

This project was manually tested using curl to ensure:

	Required fields validation (400 Bad Request)
	Non-existing resources return (404 Not Found)
	Successful creation returns (201 Created)
	Correct JSON structure in all responses

## Notes

	All endpoints were tested manually using curl
	Swagger documentation was used to verify request and response formats
	In-memory repository was used for data persistence during development and testing

  

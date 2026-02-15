# HBnB – Technical Concepts & Engineering Notes

This document summarizes the key technical concepts learned and applied during the HBnB project at Holberton School.
It reflects backend architecture, authentication mechanisms, API design, and frontend-backend integration.

## 1. Architecture & Project Structure

### Layered Architecture
The project follows a layered architecture to separate responsibilities.

Layers used:
- API Layer (Flask Routes / Namespaces)
- Service Layer (Facade)
- Models
- Database

### Why it matters
- Improves maintainability
- Separates business logic from routes
- Makes testing easier

## 2. Authentication & Authorization

### JWT (JSON Web Token)
JWT is used for stateless authentication.

Flow:
1. User sends credentials to /auth/login
2. Server verifies credentials
3. Server generates JWT token
4. Client stores token
5. Token is sent in Authorization header

Example:
Authorization: Bearer <token>

### Protected Routes
Routes are protected using:
@jwt_required()

## 3. REST API Design

The API follows REST principles.

### HTTP Methods Used
- GET → Retrieve data
- POST → Create new resource
- PUT → Update resource
- DELETE → Remove resource

Example:
POST /api/v1/reviews
GET /api/v1/places

## 4. Request Lifecycle

1. User interacts with frontend
2. JavaScript sends fetch request
3. Flask route receives request
4. Facade processes business logic
5. Database is queried
6. JSON response is returned

## 5. Frontend & Backend Separation

Backend runs on:
127.0.0.1:5000

Frontend runs on:
127.0.0.1:5500

Why different ports?
Because frontend and backend are separate services communicating via HTTP.

## 6. Database & ORM

The project uses ORM to interact with the database.

Concepts learned:
- Models
- Relationships
- Foreign Keys
- CRUD operations

## 7. Token Storage (Cookies)

The authentication token is stored in cookies.

Why?
- Automatic inclusion in requests
- Expiration control
- Secure handling (SameSite policy)

## 8. HTTP Status Codes

- 200 → Success
- 201 → Created
- 400 → Bad Request
- 401 → Unauthorized
- 404 → Not Found
- 500 → Internal Server Error

# 🛠 Browser Developer Tools (DevTools)

During Part 4 of the HBnB project, Browser Developer Tools played a critical role in debugging and validating frontend–backend integration.

---

## Console Debugging

The **Console tab** was used to:

- Identify JavaScript runtime errors
- Log API responses for validation
- Debug form submission flows
- Detect undefined variables or incorrect data handling

Example:

<pre>
 javascript
console.log(place);
</pre>

This ensured the API returned the expected structure before rendering data in the DOM.


## 🌐 Network Tab

During Part 4 of the HBnB project, the **Network tab** in Browser Developer Tools was essential for validating frontend–backend communication.

It allowed us to inspect API requests, verify authentication headers, and debug server responses in real time.

---

### 🔍 What We Used It For

- Inspect HTTP request methods (GET, POST, PUT, DELETE)
- Verify JSON request payloads
- Confirm presence of JWT in the `Authorization` header
- Check HTTP status codes
- Analyze backend error responses
- Debug CORS or connection issues

---

### 📝 Example: Submitting a Review

When submitting a review, we used:

```javascript
fetch("http://127.0.0.1:5000/api/v1/reviews", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify({
    place_id: placeId,
    text: reviewText,
    rating: rating
  })
});
```

Using the ###Network tab### , we verified:
	•	Request Method → POST
	•	Status Code → 201 Created
	•	Authorization header was included
	•	JSON body contained correct place_id
	•	The server returned the created review object


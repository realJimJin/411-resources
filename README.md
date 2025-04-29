# Waypoint

## Description
Users can save, view, and edit their favorite spots with an interactive version of Google Maps.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python -m app.main`

## Routes

---

### /login
* **Request Type:** POST
* **Purpose:** Login with an existing username and password
* **Request Body:**
```json
{
  "username": "user123",
  "password": "securepassword"
}
```
* **Response Format:** JSON
* **Success Response Example:**
  - Code: 200
  - Content:
```json
{
  "message": "Login successful"
}
```

---

### /logout
* **Request Type:** POST
* **Purpose:** Log out the current user
* **Response Format:** JSON
* **Success Response Example:**
  - Code: 200
  - Content:
```json
{
  "message": "Logged out successfully"
}
```

---

### /create-account
* **Request Type:** POST
* **Purpose:** Create a new user account
* **Request Body:**
```json
{
  "username": "newuser123",
  "password": "securepassword"
}
```
* **Response Format:** JSON
* **Success Response Example:**
  - Code: 201
  - Content:
```json
{
  "message": "Account created successfully"
}
```

---

### /update-password
* **Request Type:** POST
* **Purpose:** Change password for existing account
* **Request Body:**
```json
{
  "new_password": "securepassword2"
}
```
* **Response Format:** JSON
* **Success Response Example:**
  - Code: 200
  - Content:
```json
{
  "message": "Password updated successfully"
}
```

---

### /delete-account
* **Request Type:** DELETE
* **Purpose:** Delete the account for the logged-in user
* **Response Format:** JSON
* **Success Response Example:**
  - Code: 200
  - Content:
```json
{
  "message": "Account deleted successfully"
}
```

---

### /locations
* **Request Type:** POST
* **Purpose:** Add a new favorite location
* **Request Body:**
```json
{
  "name": "Fenway Park",
  "lat": 42.3467,
  "lng": -71.0972,
  "description": "Baseball stadium in Boston"
}
```
* **Response Format:** JSON
* **Success Response Example:**
  - Code: 201
  - Content:
```json
{
  "id": 1,
  "name": "Fenway Park",
  "lat": 42.3467,
  "lng": -71.0972,
  "description": "Baseball stadium in Boston"
}
```

* **Request Type:** GET
* **Purpose:** List all favorite locations for the user
* **Response Format:** JSON (list)
* **Success Response Example:**
  - Code: 200
  - Content:
```json
[
  {
    "id": 1,
    "name": "Fenway Park",
    "lat": 42.3467,
    "lng": -71.0972,
    "description": "Baseball stadium in Boston"
  },
  ...
]
```

---

### /locations/<id>
* **Request Type:** GET
* **Purpose:** Get details for a specific location
* **Response Format:** JSON
* **Success Response Example:**
  - Code: 200
  - Content:
```json
{
  "id": 1,
  "name": "Fenway Park",
  "lat": 42.3467,
  "lng": -71.0972,
  "description": "Baseball stadium in Boston"
}
```

* **Request Type:** PUT
* **Purpose:** Update a location
* **Request Body:**
```json
{
  "name": "Fenway Park Updated",
  "lat": 42.3467,
  "lng": -71.0972,
  "description": "Updated description"
}
```
* **Response Format:** JSON
* **Success Response Example:**
  - Code: 200
  - Content:
```json
{
  "id": 1,
  "name": "Fenway Park Updated",
  "lat": 42.3467,
  "lng": -71.0972,
  "description": "Updated description"
}
```

* **Request Type:** DELETE
* **Purpose:** Delete a location
* **Response Format:** JSON
* **Success Response Example:**
  - Code: 200
  - Content:
```json
{
  "message": "Location deleted successfully"
}
```

---

### /healthcheck
* **Request Type:** GET
* **Purpose:** Check if the application is running
* **Response Format:** JSON
* **Success Response Example:**
  - Code: 200
  - Content:
```json
{
  "status": "ok"
}
```

---

## Testing
- To run tests: `pytest tests/`

## Notes
- Fill in your Google Maps API key in `.env` before using geocoding features.
- All endpoints return JSON and require authentication except `/create-account`, `/login`, `/healthcheck`.
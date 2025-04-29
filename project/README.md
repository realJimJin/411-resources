# Waypoint

## Description
Users can save, view, and edit their favorite spots with an interactive version of Google Maps.

## Setup
1. Copy `.env.template` to `.env` and fill in your own secrets and Google Maps API key.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python -m app.main`
4. Or use Docker: `docker build -t waypoint . && docker run -p 5000:5000 waypoint`

## Routes

### /login
* Request Type: POST
* Purpose: Login with an existing username and password
* Request Body:
  - username (String): Existing username.
  - password (String): Existing password.
* Response Format: JSON
* Example Request:
```
{
  "username": "user123",
  "password": "securepassword"
}
```
* Example Response:
```
{
  "message": "Login successful"
}
```

### /logout
* Request Type: POST
* Purpose: Log out the current user
* Response Format: JSON
* Example Response:
```
{
  "message": "Logged out successfully"
}
```

### /create-account
* Request Type: POST
* Purpose: Create a new user account
* Request Body:
  - username (String)
  - password (String)
* Response Format: JSON
* Example Request:
```
{
  "username": "newuser123",
  "password": "securepassword"
}
```
* Example Response:
```
{
  "message": "Account created successfully"
}
```

### /update-password
* Request Type: POST
* Purpose: Change password for existing account
* Request Body:
  - new_password (String)
* Response Format: JSON
* Example Request:
```
{
  "new_password": "securepassword2"
}
```
* Example Response:
```
{
  "message": "Password updated successfully"
}
```

### /delete-account
* Request Type: DELETE
* Purpose: Delete the account (not implemented in code above, add if needed)
* Request Body:
  - username (String)
  - password (String)
* Response Format: JSON
* Example Request:
```
{
  "username": "newuser123",
  "password": "securepassword"
}
```
* Example Response:
```
{
  "message": "Account deleted successfully"
}
```

### /locations
* Request Type: POST
* Purpose: Add a new favorite location
* Request Body:
  - name (String)
  - lat (float)
  - lng (float)
  - description (String, optional)
* Response Format: JSON
* Example Request:
```
{
  "name": "Fenway Park",
  "lat": 42.3467,
  "lng": -71.0972,
  "description": "Baseball stadium in Boston"
}
```
* Example Response:
```
{
  "id": 1,
  "name": "Fenway Park",
  "lat": 42.3467,
  "lng": -71.0972,
  "description": "Baseball stadium in Boston"
}
```

* Request Type: GET
* Purpose: List all favorite locations for the user
* Response Format: JSON (list)

### /locations/<id>
* Request Type: GET
* Purpose: Get details for a specific location
* Response Format: JSON

* Request Type: PUT
* Purpose: Update a location
* Request Body: Any updatable field (name, lat, lng, description)
* Response Format: JSON

* Request Type: DELETE
* Purpose: Delete a location
* Response Format: JSON

### /healthcheck
* Request Type: GET
* Purpose: Check if the application is running
* Response Format: JSON
* Example Response:
```
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
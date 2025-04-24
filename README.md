# 411-resources
Description: Users can save, view, and edit their favorite spots with an interactive version of Google Maps. 

Routes: 
/login: 
Request Type: GET
Purpose: Login with an existing username and password
Request Body:
username (String): Existing username.
password (String): Existing password (tied to the user).
newPassword (String): New password 
Response Format: JSON
Success Response Example:
Code: 200
Content: { "message": "Account logged in successfully" }
 Example Request:
{
"username": "newuser123",
"password": "securepassword"

}
Example Response:
{
"message": "Account logged in successfully",
"status": "200"
}
/logout: 
/create-account: 
Request Type: POST
Purpose: Creates a new user account with a username and password.
Request Body:
username (String): Existing username.
password (String): Existing password (tied to the user).
newPassword (String): New password 
Response Format: JSON
Success Response Example:
Code: 200
Content: { "message": "Account created successfully" }
 Example Request:
{
"username": "newuser123",
"password": "securepassword"

}
Example Response:
{
"message": "Account created successfully",
"status": "200"
}

/update-password: 
Request Type: PATCH
Purpose: Change password for existing account.
Request Body:
username (String): Existing username.
password (String): Current password.
newPassword (String) : User’s new Password 
Response Format: JSON
Success Response Example:
Code: 200
Content: { "message": "Account password updated successfully" }
 Example Request:
{
"username": "newuser123",
"password": "securepassword"
“newPassword”: "securepassword2"
}
Example Response:
{
"message": "Account password changed successfully",
}

/delete-account:
Request Type: Delete
Purpose: Deletes account from username and password
Request Body:
username (String): Existing username.
password (String): Existing password (tied to the user).
Response Format: JSON
Success Response Example:
Code: 200
Content: { "message": "Account deleted successfully" }
 Example Request:
{
"username": "newuser123",
"password": "securepassword"
}
Example Response:
{
"message": "Account deleted successfully",
"status": "200"
}

/healthcheck:



What the application does at a high level
A description of each route (example on ed discussion):	
Route Name and Path
Request Type
GET, POST, PUT, DELETE
Purpose
Request Format
GET parameters
POST / PUT / DELETE body
Response Format
JSON keys and value types	
Example
Request in the form of JSON body or cURL command
Associated JSON response


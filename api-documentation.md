# API Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Error Handling](#error-handling)
3. [User Class](#user-class)
    - 3.1 [List of users or details](#methods)
        - 3.1.1[Get user](#get-users)
        - 3.1.2[Post user](#post-user)
        - 3.1.3[Put user](#put-user)
        - 3.1.4[Delete user](#delete-user)
   
## Introduction
Welcome to the API documentation. This API documentation provides detailed information about the endpoints and models for a user and event management system. It includes information on how to use each endpoint, expected input data, success responses, and HTTP status codes

## Error Handling
The API handles errors gracefully and returns JSON responses with appropriate status codes and error messages. Here are some common error responses:

###  400 Bad Request: 
- **status_code**: 400,
- **response_body**:

```JSON 
{
    "error": "Bad Request",
    "message": "Invalid input data"
}
```

### 401 Unauthorized:
- **status_code**: 401
- **response_body**:
```JSON
{
    "error": "Unauthorized",
    "message": "Authentication failed"
}
```
### 404 Not Found:
**status_code**: 404
**response_body**:
```JSON
{
    "error": "Not Found",
    "message": "User not found"
}
```
### 500 Internal Server Error:
**status_code**: 500
**response_body**:
```JSON
{
    "error": "Internal Server Error",
    "message": "An unexpected error occurred"
}
```

## User Class
- **Endpoint**: /api/users
- **Description**:API for managing user information.

### Methods

#### GET USERS
- **Description**: Retrieve a list of users or details of a specific user.
- **URL**: /api/users
- **Response**:
  - **status_code**: 200
  - **response_body**:
    ```JSON
    {
      "users": [
        {
            "id": "users_id",
            "username": "username",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "user email",
            "section_order":"section_order",
            "password": "password",
            "is_verified": "bool",
            "two_factor_auth": "bool",
            "provider": "str",
            "profile_pic": "user picture",
            "refresh_token": "refresh_token",
            "created_at": "datetime"
        },

      ]
    }
    ```
- **Error Responses**:
    - **400 Bad Request**:
        - **Status Code**: 400
        - **Response Body**:
        ```JSON
        {
          "error": "Bad Request",
          "message": "Invalid input data."
        }
        ``` 

#### POST USER

- **Description**: Create a new user.
- **URL**: /api/users
- **Response**:
    - **Status Code**: 201
    - **Response_body**:
    ```JSON
    {
        "message": "User created successfully",
        "user": {
        "id": "users_id",
        "username": "username",
        "first_name": "firstname",
        "last_name": "lastname",
        "email": "user email",
        "section_order":"section_order",
        "password": "password",
        "is_verified": "bool",
        "two_factor_auth": "bool",
        "provider": "str",
        "profile_pic": "user picture",
        "refresh_token": "refresh_token",
        "created_at": "datetime"
        }  
    }
     ```
- **401 Unauthorized**:
- **status_code**: 401
- **response_body**:
```JSON
{
    "error": "Unauthorized",
    "message": "Authentication failed"
}
```

#### PUT USER
- **Description**: Update user information.
- **URL**: /api/users/<user_id>
- **status_code**: 200
- **Request Body**:
 ```JSON
{
  "message": "User updated successfully",
    "user": {
        "id": "users_id",
        "username": "username",
        "first_name": "firstname",
        "last_name": "lastname",
        "email": "user email",
        "section_order":"section_order",
        "password": "password",
        "is_verified": "bool",
        "two_factor_auth": "bool",
        "provider": "str",
        "profile_pic": "user picture",
        "refresh_token": "refresh_token",
        "created_at": "datetime"
    }
}
```
- **404 Not Found**:
- **status_code**: 404
- **response_body**:
```JSON
{
    "error": "Not Found",
    "message": "User not found"
}
```

#### DELETE USER
- **Description**: Delete a user.
- **URL**: /api/users/<user_id>
- **Response**:
- **status_code**: 204
- **response_body**: null

- **500 Internal Server Error**:
- **status_code: 500**
- **response_body:**
```JSON
{
    "error": "Internal Server Error",
    "message": "An unexpected error occurred"
}
```





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
4. [Shop Class](#shop-class-template)
    - 4.1[Class overview](#class-overview)
    - 4.2[Attributes](#attributes)
    - 4.3[Methods](#methods-1)
    - 4.4[Usage](#usage)
5. [Product management](#product-class)
    - 5.1[methods](#methods-2)
        - 5.1.1[Get product](#get-product)
        - 5.1.2[Post product](#post-product)
        - 5.1.3[Attributes](#attribute-descriptions)

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
## Shop Class Template

This is a template for the `Shop` class, which appears to be part of a larger Python project. The `Shop` class is defined within the context of a database, possibly using SQLAlchemy.

### Class Overview

The `Shop` class represents a shop in a system. It has various attributes and methods for managing shop-related data. Here's an overview of the class:

#### Attributes
- `id`: A unique identifier for the shop.
- `merchant_id`: A string representing the ID of the merchant who owns the shop. It's a foreign key referencing the "user" table.
- `name`: The name of the shop.
- `policy_confirmation`: A boolean indicating whether the shop has confirmed its policy.
- `restricted`: An enumeration indicating the restriction status of the shop (`'no'`, `'temporary'`, `'permanent'`).
- `admin_status`: An enumeration indicating the admin status of the shop (`'pending'`, `'review'`, `'approved'`, `'blacklist'`).
- `is_deleted`: An enumeration indicating the status of the shop (`'active'`, `'temporary'`).
- `reviewed`: A boolean indicating whether the shop has been reviewed.
- `rating`: A numeric rating for the shop.

#### Methods
- `__init__(self, merchant_id, name, policy_confimation, restricted, admin_status, is_deleted, reviewed, rating)`: Constructor method to initialize the `Shop` object with the provided attributes.
- `__repr__(self)`: Returns an official representation of the object as a dictionary.
- `format(self)`: Formats the object's attributes as a dictionary.

#### Usage
To create a new `Shop` object, you can use the constructor as follows:
```python
shop = Shop(merchant_id, name, policy_confirmation, restricted, admin_status, is_deleted, reviewed, rating)
```

## product class
- **Endpoint**: "/products"
- **Description**:This API provides endpoints for managing products..

### Methods
#### GET product
- **Description:** Retrieve a list of products.
- **Response:**
  - **Status Code:** 200
  - **Response Body:**
    ```json
    {
        "message": "List of products retrieved successfully.",
        "products": [
            {
                "id": "product_id",
                "shop_id": "shop_id",
                "rating_id": "rating_id",
                "image_id": "image-id",
                "category_id": "catergory_id",
                "name": "username",
                "description": "notes",
                "quantity": "amount",
                "price": "price",
                "discount_price": "dis_price",
                "tax": "tax",
                "admin_status": "status",
                "is_deleted": "delete",
                "is_published": "boolean",
                "currency": "currency",
                "created_at": "time_created in UTCNow",
                "updated_at": "time_updated in UTCNow"
            }
        ]
    }
    ```

#### POST product
- **Description:** Create a new product.
- **Response:**
  - **Status Code:** 201
  - **Response Body:**
    ```json
    {
        "id": "product_id",
        "shop_id": "shop_id",
        "rating_id": "rating_id",
        "image_id": "image-id",
        "category_id": "catergory_id",
        "name": "username",
        "description": "notes",
        "quantity": "amount",
        "price": "price",
        "discount_price": "dis_price",
        "tax": "tax",
        "admin_status": "status",
        "is_deleted": "delete",
        "is_published": "boolean",
        "currency": "currency",
        "created_at": "time_created in UTCNow",
        "updated_at": "time_updated in UTCNow"
    }
#### Attribute Descriptions
##### shop_id
- **Description:** ID of the shop to which the product belongs.
- **Type:** string

##### rating_id
- **Description:** ID of the product's rating.
- **Type:** string

##### image_id
- **Description:** ID of the product's image.
- **Type:** string

##### category_id
- **Description:** ID of the product's category.
- **Type:** string

##### name
- **Description:** Name of the product.
- **Type:** string

##### description
- **Description:** Description of the product.
- **Type:** string

##### quantity
- **Description:** Quantity of the product available.
- **Type:** integer

##### price
- **Description:** Price of the product.
- **Type:** numeric

#####  discount_price
- **Description:** Discounted price of the product.
- **Type:** numeric

#####  tax
- **Description:** Tax rate applied to the product.
- **Type:** numeric

#####  admin_status
- **Description:** Admin status of the product.
- **Type:** string
- **Enum:** ["pending", "review", "approved", "blacklist"]

##### is_deleted
- **Description:** Product status indicating whether it's active or temporary.
- **Type:** string
- **Enum:** ["active", "temporary"]

##### is_published
- **Description:** Flag indicating whether the product is published.
- **Type:** boolean

##### currency
- **Description:** Currency code for the product's price.
- **Type:** string




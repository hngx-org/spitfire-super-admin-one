# Spitfire Superadmin API Documentation

![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

Welcome to the official documentation for the Spitfire Superadmin API. This RESTful API is designed to provide administrators with comprehensive tools for managing shops, products, vendors, and ensuring the health of the system. Please refer to this documentation to understand the available endpoints, their functionality, and how to use them effectively.

## Table of Contents

- [1. Introduction](#introduction)
- [2. Features](#features)
- [3. Technologies Used](#technologies-used)
- [4. Getting Started](#getting-started)
  - [4.1 Prerequisites](#prerequisites)
     - [4.1.1 Clone The Repository](#clone-the-repository)
     - [4.1.2 Install Dependencies](#install-the-dependencies)
     - [4.1.3 Configure Environment Variables](#configure-environment-variables)
  - [4.2 Usage](#usage)
- [5. API Endpoints](#api-endpoints)
- [6. Database Schema](#database-schema)
- [7. Authentication](#authentication)
- [8. Error Handling](#error-handling)
- [9. Testing](#testing)
- [10. Deployment](#deployment)
- [11. Contributing](#contributing)
   -[11.1 Commit Convention](#commit-convention)
- [12. License](#license)
- [13. Acknowledgments](#acknowledgments)

## 1. Introduction

The Spitfire Superadmin API is a powerful system administration tool designed to provide administrators with complete control over shops, products, and vendors. It enables you to ensure the health and stability of the system. This API is essential for managing an e-commerce platform effectively.


## 2. Features

All API endpoints are meant for the superadmin and therefore require a verification token to access.
Includes endpoints for product and shop management.

## 3. Technologies Used

Utilizes technologies like Python, Flask, SQLAlchemy, and more.

## 4. Getting Started

### 4.1 Prerequisites
#### 4.1.1 Clone The Repository

To get started with the local development environment, clone the repository:

```bash
$ git clone https://github.com/hngx-org/spitfire-super-admin-one.git
$ cd super_admin_1
```

#### 4.1.2 Install Dependencies

You can set up the environment using either `venv` or `pipenv`. Here are instructions for both:

Using `venv`:

```bash
# create Virtual Environment
$ python3 -m venv venv

# Activate Virtual Env
$ source venv/bin/activate

# Install Dependencies
$ pip install -r requirements.txt
```

Using `pipenv`:

```bash
$ pip install pipenv

# create virtuel environment
$ pipenv --python 3.10

# Activate virtual env
$ pipenv shell

# install dependencies in requirements.txt or pipfile
$ pipenv install
```

#### 4.1.3 Configure Environment Variables

Make sure to set the following environment variables:

    SECRET_KEY: [Your Secret Key]
    SQLALCHEMY_DATABASE_URI: [Your Database URI]

### 4.1.4 Usage

```bash
$ python3 run.py
```

## 5. API Endpoints

### 5.1 Shop

The Shop endpoints allow administrators to manage shops and vendors effectively. 

#### 5.1.1 Get Information from the Shop Endpoint

- **GET**: `/shop/endpoint`
  - **Summary**: Get information from the shop endpoint
  - **Description**: This endpoint retrieves information from the shop endpoint. The user ID is automatically provided by the authorization logic.
  - **Responses**:
    - `200`: Successful response
      - Message: "This is the shop endpoint for user ID: <user_id>"
    - `401`: Unauthorized - Invalid or missing authentication token
    - `403`: Forbidden - User does not have permission to access the resource

#### 5.1.2 Get information related to all shops

- **GET**: `/shop/all`
  - **Summary**: Get information related to all shops
  - **Description**: This endpoint retrieves information related to all shops in the system. Requires admin authentication.
  - **Responses**:
    - `200`: Successful response
      - Message: "All shops request successful"
      - Data: Array of shop details
    - `401`: Unauthorized - Invalid or missing authentication token
    - `403`: Forbidden - User does not have permission to access the resource
    - `500`: Internal Server Error

#### 5.1.3 Get information related to a specific shop

- **GET**: `/shop/{shop_id}`
  - **Summary**: Get information related to a specific shop
  - **Description**: This endpoint retrieves information related to a specific shop identified by the provided shop ID. Requires admin authentication.
  - **Parameters**:
    - `shop_id` (Path Parameter, Required): Unique identifier for the shop
  - **Responses**:
    - `200`: Successful response
      - Message: "Shop request successful"
      - Data: Shop details
    - `401`: Unauthorized - Invalid or missing authentication token
    - `403`: Forbidden - User does not have permission to access the resource
    - `404`: Not Found - Shop with the given ID not found
    - `500`: Internal Server Error

#### 5.1.4 Ban a vendor/shop by ID

- **PUT**: `/shop/ban_vendor/{vendor_id}`
  - **Summary**: Ban a vendor/shop by ID
  - **Parameters**:
    - `vendor_id` (Path Parameter, Required): Unique identifier for the vendor
    - `reason` (Request Body, Required): Ban reason
  - **Responses**:
    - `201`: Vendor banned successfully
      - Message: "Vendor account banned temporarily."
      - Vendor details
      - Reason
    - `400`: Bad request - Vendor is already banned or missing reason
    - `404`: Vendor not found
    - `409`: Conflict - Vendor is already banned
    - `500`: Internal Server Error

#### 5.1.5 Get a list of all temporarily banned vendors

- **GET**: `/shop/banned_vendors`
  - **Summary**: Get a list of all temporarily banned vendors
  - **Responses**:
    - `200`: Successful response
      - Message: "Banned vendors retrieved successfully."
      - Banned vendors

#### 5.1.6 Unban a vendor by ID

- **PUT**: `/shop/unban_vendor/{vendor_id}`
  - **Summary**: 
  - **Parameters**:
    - `vendor_id` (Path Parameter, Required): Unique identifier for the vendor
  - **Responses**:
    - `200`: Vendor unbanned successfully
      - Status: "Success"
      - Message: "Vendor unbanned successfully."
      - Vendor details
    - `404`: Vendor not found
    - `400`: Vendor's shop is not active
    - `500`: Internal Server Error

#### 5.1.7 Restore a temporarily deleted shop by ID

- **PATCH**: `/shop/restore_shop/{shop_id}`
  - **Summary**: Restore a temporarily deleted shop by ID
  - **Parameters**:
    - `shop_id` (Path Parameter, Required): Unique identifier for the shop
  - **Responses**:
    - `200`: Shop restored successfully
      - Message: "Shop restored successfully"
    - `404`: Invalid Shop
    - `400`: Invalid JSON Data

#### 5.1.8 Temporarily delete a shop and its associated products

- **PATCH**: `/shop/delete_shop/{shop_id}`
  - **Summary**: Temporarily delete a shop and its associated products
  - **Parameters**:
    - `shop_id` (Path Parameter, Required): Unique identifier for the shop
  - **Responses**:
    - `204`: Shop temporarily deleted
    - `404`: Invalid Shop
    - `500`: Internal Server Error

#### 5.1.9 Permanently delete a shop and its associated products

- **DELETE**: `/shop/permanent_delete_shop/{shop_id}`
  - **Summary**: Permanently delete a shop and its associated products
  - **Parameters**:
    - `shop_id` (Path Parameter, Required): Unique identifier for the shop
  - **Responses**:
    - `204`: Shop permanently deleted
    - `404`: Invalid Shop
    - `500`: Internal Server Error

#### 5.1.10 Retrieve temporarily deleted vendors

- **Get**: `/shop/temporarily_deleted_vendors`
  -**Summary**: Retrieve temporarily deleted vendors
  -**Responses**:
    - `200` : Successful response
      - Message: "Temporarily deleted vendors retrieved successfully"
    - `500` : Internal Server Error

#### 5.1.11 Retrieve details of a temporarily deleted vendor

- **Get**: `/shop/temporarily_deleted_vendor/{vendor_id}`
  -**Summary**: Retrieve details of a temporarily deleted vendor
  - **Parameters**:
    - `vendor_id` (Path Parameter, Required): Unique identifier for the vendor
  - **Responses**:
    - `200`: Temporarily deleted vendor details retrieved successfully
    - `404`: Temporarily deleted vendor not found
    - `500`: Internal Server Error

#### 5.1.12 Get all sanctioned shops

- **Get**: `/shop/sanctioned`
  -**Summary**: Returns a list of all sanctioned shops
  -**Responses**:
    - `200`: Sanctioned shops retrieved successfully
    - `500`: Internal Server Error

### 5.2 Product

#### 5.2.1 Get information related to all products

- **GET**: `/product/all`
  - **Summary**: Get information related to all products
  - **Description**: Returns a list of all products in the system.
  - **Responses**:
    - `200`: Successful response
      - Message: "All products retrieved successfully."
      - Data: List of products
    - `500`: Internal Server Error

#### 5.2.2 Get information related to a product

- **GET**: `/product/{product_id}`
  - **Summary**: Get information related to a product
  - **Description**: Returns details of a specific product.
  - **Parameters**:
    - `product_id` (Path Parameter, Required): Unique identifier for the product
  - **Responses**:
    - `200`: Successful response
      - Message: "Product details retrieved successfully."
      - Data: Product details
    - `404`: Product not found
    - `500`: Internal Server Error

#### 5.2.3 Sanction a product

- **PATCH**: `/product/sanction/{product_id}`
  - **Summary**: Sanction a product by setting its status to 'suspended'
  - **Parameters**:
    - `product_id` (Path Parameter, Required): Unique identifier for the product
  - **Responses**:
    - `200`: Product sanctioned successfully
      - Message: "Product sanctioned successfully."
      - Product details
    - `404`: Product not found
    - `409`: Conflict - Product is already sanctioned
    - `500`: Internal Server Error

#### 5.2.4 Get product statistics

- **GET**: `/product/product_statistics`
  - **Summary**: Get statistics about products
  - **Responses**:
    - `200`: Product statistics retrieved successfully
      - TotalProducts: Total number of products
      - SanctionedProducts: Total number of sanctioned products
      - DeletedProducts: Total number of deleted products
    - `400`: Bad request
    - `500`: Internal Server Error

#### 5.2.5 Temporarily delete a product by ID

- **PATCH**: `/product/delete_product/{id}`
  - **Summary**: Temporarily delete a product by ID
  - **Parameters**:
    - `id` (Path Parameter, Required): Unique identifier for the product
  - **Responses**:
    - `204`: Product temporarily deleted
    - `404`: Invalid Product
    - `500`: Internal Server Error

#### 5.2.6 Permanently delete a product by ID

- **DELETE**: `/product/permanent_delete_product/{id}`
  - **Summary**: Permanently delete a product by ID
  - **Parameters**:
    - `id` (Path Parameter, Required): Unique identifier for the product
  - **Responses**:
    - `204`: Product permanently deleted
    - `404`: Invalid Product
    - `500`: Internal Server Error

#### 5.2.7 Restore a temporarily deleted product

- **PATCH**: `/product/restore_product/{product_id}`
  - **Summary**: Restore a temporarily deleted product by id
  - **Parameters**:
    -`id` (Path Parameter, Required): Unique identifier for the product
  - **Responses**:
    - `200`: Product restored successfully
    - `404`: Invalid Product

#### 5.2.8 Approve a product

- **PATCH**: `/product/approve_product/{product_id}`
  - **Summary**: Approve a product by changing the admin status
  - **Parameters**:
    -`id` (Path Parameter, Required): Unique identifier for the product
  - **Responses**:
    - `201`: Product approved successfully
    - `404`: Product not found
    - `409`: Conflict. Action already carried out on this Product
    - `500`: Internal Server Error

#### 5.2.9 Retrieve temporarily deleted products

- **GET**: `/product/temporarily_deleted_products`
- **Responses**:
    - `200`: Successful response
    - `500`: Internal Server Error

#### 5.2.10 Download product logs

- **GET**: `product/download/log`
- **Responses**:
  - `200`: Successful response
  - `204`: No log entry exists

### 5.3 Default

#### 5.3.1 Check the availability of specified API endpoints

- **GET**: `/health/`
- **Response**:
  - `200`: Successful health check
  - `500`: Internal Server Error

#### 5.3.2 Retrieve the last health check log entry

- **GET**: `/health/last_check`
- **Response**:
  - `200`: Successful retrieval of the last health check log entry
  - `404`: No health check logs available
  - `500`: Internal Server Error

### 5.4 Test

#### 5.4.1 Create a new user

- **POST**: `/test/user/create`
- **Response**:
  - `201`: User created successfully
  - `400`: Bad request - Invalid input data

#### 5.4.2 Get all users

- **GET**: `/test/user`
- **Response**:
  - `200`: Successful response

#### 5.4.3 Delete a user by ID

- **DELETE**: `/test/user/{user_id}`
- **Parameters**:
  -`user_id` (Path Parameter, Required): Unique identifier for the user
- **Response**:
  - `200`: User deleted successfully
  - `404`: User not found


#### 5.4.4 Cretae a new shop for a user

- **POST**: `/test/user/{user_id}/shop`
- **Parameters**:
  -`user_id` (Path Parameter, Required): Unique identifier for the user
- **Response**:
  - `201`: Shop created successfully
  - `400`: Bad request - Invalid input data

#### 5.4.5 Get all shops

- **GET**: `/test`
- **Response**:
  - `200`: Successful response

#### 5.4.6 Get a specific shop by ID

- **GET**: `/test/{shop_id}`
- **Parameters**:
  -`shop_id` (Path Parameter, Required): Unique identifier for the shop
- **Response**:
  - `200`: Shop details retrieved successfully
  - `404`: Shop not found


## Database Schema

The Spitfire Superadmin API utilizes a PostgreSQL database to store and manage data efficiently. This schema defines the structure and relationships of the tables used to store information related to shops, products, vendors, and more.
Tables: Shop table
        Product table
        Vendor table

## Authentication

Every endpoint in this API is meant to be used by the super admin user. To access any of the endpoints, you will need an authentication token.

## Error Handling


> Errors are returned as JSON objects in the following format with their error code

```json
{
  "error": "error name",
  "message": "error description"
}
```

<br>

The API will return 5 error types, with diffreent descriptions when requests fail;

- 400: Request unprocessable
- 403: Forbidden
- 404: resource not found
- 422: Bad Request
- 429: Too Many Requests(rate limiting)
- 500: Internal server error

<br>

## Testing


**Note:** ensure you are connected to the internet before running tests and are in `spitfire-events` directory

```bash
# install test suite and HTTP requests library
$ pip install requests pytest

cd super_admin_1
$ pytest tests\* -v
```
## Deployment

The super admin 1 App is hosted for live testing at [https://spitfire-superadmin-1.onrender.com].

## Contributing

### Commit Convention

Before you create a Pull Request, please check whether your commits comply with
the commit conventions used in this repository.

When you create a commit we kindly ask you to follow the convention
`category(scope or module): message` in your commit message while using one of
the following categories:

- `feat / feature`: all changes that introduce completely new code or new
  features
- `fix`: changes that fix a bug (ideally you will additionally reference an
  issue if present)
- `refactor`: any code related change that is not a fix nor a feature
- `docs`: changing existing or creating new documentation (i.e. README, docs for
  usage of a lib or cli usage)
- `build`: all changes regarding the build of the software, changes to
  dependencies or the addition of new dependencies
- `test`: all changes regarding tests (adding new tests or changing existing
  ones)
- `ci`: all changes regarding the configuration of continuous integration (i.e.
  github actions, ci system)
- `chore`: all changes to the repository that do not fit into any of the above
  categories.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Appreciation and acknowledgments to contributors, libraries, or resources that helped in developing the API.

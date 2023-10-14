# Spitfire Superadmin API

**Version**: 1.0

## Introduction

This document provides an overview of the Spitfire Superadmin API, which is used for managing shops, products, and vendors. The API offers various endpoints to perform actions such as retrieving shop information, managing products, and handling vendor-related operations. The API is designed for super admin users.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
     - [Clone The Repository](#clone-the-repository)
     - [Install Dependencies](#install-the-dependencies)
     - [Configure Environment Variables](#configure-environment-variables)
  - [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Authentication](#authentication)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
   -[Commit Convention](#commit-convention)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

All API endpoints are meant for the superadmin and therefore require a verification token to access.
Includes endpoints for product and shop management.

## Technologies Used

Utilizes technologies like Python, Flask, SQLAlchemy, and more.

## Getting Started

### Prerequisites
#### Clone The Repository

To get started with the local development environment, clone the repository:

```bash
$ git clone https://github.com/hngx-org/spitfire-super-admin-one.git
$ cd super_admin_1
```

#### Install Dependencies

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

#### Configure Environment Variables

Make sure to set the following environment variables:

    SECRET_KEY: [Your Secret Key]
    SQLALCHEMY_DATABASE_URI: [Your Database URI]

### Usage

```bash
$ python3 run.py
```

## API Endpoints

### Shop

#### `/shop/endpoint`

- **GET**: Get information from the shop endpoint
  - **Summary**: Get information from the shop endpoint
  - **Description**: This endpoint retrieves information from the shop endpoint. The user ID is automatically provided by the authorization logic.
  - **Responses**:
    - `200`: Successful response
      - Message: "This is the shop endpoint for user ID: <user_id>"
    - `401`: Unauthorized - Invalid or missing authentication token
    - `403`: Forbidden - User does not have permission to access the resource

#### `/shop/all`

- **GET**: Get information related to all shops
  - **Summary**: Get information related to all shops
  - **Description**: This endpoint retrieves information related to all shops in the system. Requires admin authentication.
  - **Responses**:
    - `200`: Successful response
      - Message: "All shops request successful"
      - Data: Array of shop details
    - `401`: Unauthorized - Invalid or missing authentication token
    - `403`: Forbidden - User does not have permission to access the resource
    - `500`: Internal Server Error

#### `/shop/{shop_id}`

- **GET**: Get information related to a specific shop
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

#### `/shop/ban_vendor/{vendor_id}`

- **PUT**: Ban a vendor/shop by ID
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

#### `/shop/banned_vendors`

- **GET**: Get a list of all temporarily banned vendors
  - **Summary**: Get a list of all temporarily banned vendors
  - **Responses**:
    - `200`: Successful response
      - Message: "Banned vendors retrieved successfully."
      - Banned vendors

#### `/shop/unban_vendor/{vendor_id}`

- **PUT**: Unban a vendor by ID
  - **Summary**: Unban a vendor by ID
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

#### `/shop/restore_shop/{shop_id}`

- **PATCH**: Restore a temporarily deleted shop by ID
  - **Summary**: Restore a temporarily deleted shop by ID
  - **Parameters**:
    - `shop_id` (Path Parameter, Required): Unique identifier for the shop
  - **Responses**:
    - `200`: Shop restored successfully
      - Message: "Shop restored successfully"
    - `404`: Invalid Shop
    - `400`: Invalid JSON Data

#### `/shop/delete_shop/{shop_id}`

- **PATCH**: Temporarily delete a shop and its associated products
  - **Summary**: Temporarily delete a shop and its associated products
  - **Parameters**:
    - `shop_id` (Path Parameter, Required): Unique identifier for the shop
  - **Responses**:
    - `204`: Shop temporarily deleted
    - `404`: Invalid Shop
    - `500`: Internal Server Error

#### `/shop/permanent_delete_shop/{shop_id}`

- **DELETE**: Permanently delete a shop and its associated products
  - **Summary**: Permanently delete a shop and its associated products
  - **Parameters**:
    - `shop_id` (Path Parameter, Required): Unique identifier for the shop
  - **Responses**:
    - `204`: Shop permanently deleted
    - `404`: Invalid Shop
    - `500`: Internal Server Error

### Product

#### `/product/all`

- **GET**: Get information related to all products
  - **Summary**: Get information related to all products
  - **Description**: Returns a list of all products in the system.
  - **Responses**:
    - `200`: Successful response
      - Message: "All products retrieved successfully."
      - Data: List of products
    - `500`: Internal Server Error

#### `/product/{product_id}`

- **GET**: Get information related to a product
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

#### `/product/sanction/{product_id}`

- **PATCH**: Sanction a product
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

#### `/product/product_statistics`

- **GET**: Get product statistics
  - **Summary**: Get statistics about products
  - **Responses**:
    - `200`: Product statistics retrieved successfully
      - TotalProducts: Total number of products
      - SanctionedProducts: Total number of sanctioned products
      - DeletedProducts: Total number of deleted products
    - `400`: Bad request
    - `500`: Internal Server Error

#### `/product/delete_product/{id}`

- **PATCH**: Temporarily delete a product by ID
  - **Summary**: Temporarily delete a product by ID
  - **Parameters**:
    - `id` (Path Parameter, Required): Unique identifier for the product
  - **Responses**:
    - `204`: Product temporarily deleted
    - `404`: Invalid Product
    - `500`: Internal Server Error

#### `/product/permanent_delete_product/{id}`

- **DELETE**: Permanently delete a product by ID
  - **Summary**: Permanently delete a product by ID
  - **Parameters**:
    - `id` (Path Parameter, Required): Unique identifier for the product
  - **Responses**:
    - `204`: Product permanently deleted
    - `404`: Invalid Product
    - `500`: Internal Server Error

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

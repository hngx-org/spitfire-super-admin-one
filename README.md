# team-spitfire-super-admin-one
# Spitfire Superadmin API

This is the documentation for the Spitfire Superadmin API, version 1.0.

[![Powered by Flasgger](https://img.shields.io/badge/Powered%20by-Flasgger-0.9.7.1-blue.svg)](https://flasgger.0.9.7.1)

## Table of Contents

- [Introduction](#introduction)
- [API Endpoints](#api-endpoints)
  - [Shop](#shop)
  - [Product](#product)
  - [Health](#health)
  - [Test](#test)
- [Models](#models)

## Introduction

This API documentation provides information on the Spitfire Superadmin API. It includes various endpoints for managing shops, products, performing health checks, and testing user-related operations.

## API Endpoints

### Shop

#### GET /shop/endpoint

Get information from the shop endpoint.

#### GET /shop/all

Get information related to all shops.

#### GET /shop/{shop_id}

Get information related to a specific shop.

#### PUT /shop/ban_vendor/{vendor_id}

Ban a vendor/shop by ID.

#### GET /shop/banned_vendors

Get a list of all temporarily banned vendors.

#### PUT /api/shop/unban_vendor/{vendor_id}

Unban a vendor by ID.

#### PATCH /shop/restore_shop/{shop_id}

Restore a temporarily deleted shop by ID.

#### PATCH /shop/delete_shop/{shop_id}

Temporarily delete a shop and its associated products.

#### DELETE /shop/delete_shop/{shop_id}

Permanently delete a shop and its associated products.

#### GET /shop/temporarily_deleted_vendors

Retrieve temporarily deleted vendors.

#### GET /shop/temporarily_deleted_vendor/{vendor_id}

Retrieve details of a temporarily deleted vendor.

#### GET /shop/sanctioned

Get all sanctioned shops.

### Product

#### GET /product/all

Get information related to all products.

#### GET /product/{product_id}

Get information related to a product.

#### PATCH /product/sanction/{product_id}

Sanction a product.

#### GET /product/product_statistics

Get product statistics.

#### PATCH /product/delete_product/{id}

Temporarily delete a product by ID.

#### DELETE /product/delete_product/{id}

Permanently delete a product by ID.

#### PATCH /product/restore_product/{product_id}

Restore a temporarily deleted product by ID.

#### PATCH /product/approve_product/{product_id}

Approve a product.

#### GET /product/temporarily_deleted_products

Retrieve temporarily deleted products.

#### GET /product/download/log

Download product logs.

### Health

#### GET /health/

Check the availability of specified API endpoints.

#### GET /health/last_check

Retrieve the last health check log entry.

### Test

#### POST /test/user/create

Create a new user.

#### GET /test/user

Get all users.

#### DELETE /test/user/<user_id>

Delete a user by ID.

#### POST /test/user/<user_id>/shop

Create a new shop for a user.

#### GET /test

Get all shops.

#### GET /test/<shop_id>

Get a specific shop by ID.

## Models

[Powered by Flasgger 0.9.7.1]


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

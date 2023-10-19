# Spitfire Superadmin API

![Version](https://img.shields.io/badge/version-1.0-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

This is the official documentation for the Spitfire Superadmin API, version 1.0.

## Table of Contents

- [Introduction](#introduction)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
  - [Shop](#shop)
    - [Get Information from the Shop Endpoint](#get-information-from-the-shop-endpoint)
    - [Get Information Related to All Shops](#get-information-related-to-all-shops)
    - [Get Information Related to a Specific Shop](#get-information-related-to-a-specific-shop)
    - [Ban a Vendor/Shop by ID](#ban-a-vendorshop-by-id)
    - [Get a List of All Temporarily Banned Vendors](#get-a-list-of-all-temporarily-banned-vendors)
    - [Unban a Vendor by ID](#unban-a-vendor-by-id)
    - [Restore a Temporarily Deleted Shop by ID](#restore-a-temporarily-deleted-shop-by-id)
    - [Temporarily Delete a Shop and Its Associated Products](#temporarily-delete-a-shop-and-its-associated-products)
    - [Permanently Delete a Shop and Its Associated Products](#permanently-delete-a-shop-and-its-associated-products)
    - [Retrieve Temporarily Deleted Vendors](#retrieve-temporarily-deleted-vendors)
    - [Retrieve Details of a Temporarily Deleted Vendor](#retrieve-details-of-a-temporarily-deleted-vendor)
    - [Get All Sanctioned Shops](#get-all-sanctioned-shops)
  - [Product](#product)
    - [Get Information Related to All Products](#get-information-related-to-all-products)
    - [Get Information Related to a Product](#get-information-related-to-a-product)
    - [Sanction a Product](#sanction-a-product)
    - [Get Product Statistics](#get-product-statistics)
    - [Temporarily Delete a Product by ID](#temporarily-delete-a-product-by-id)
    - [Permanently Delete a Product by ID](#permanently-delete-a-product-by-id)
    - [Restore a Temporarily Deleted Product by ID](#restore-a-temporarily-deleted-product-by-id)
    - [Approve a Product](#approve-a-product)
    - [Retrieve Temporarily Deleted Products](#retrieve-temporarily-deleted-products)
    - [Download Product Logs](#download-product-logs)
  - [Health](#health)
    - [Check the Availability of Specified API Endpoints](#check-the-availability-of-specified-api-endpoints)
    - [Retrieve the Last Health Check Log Entry](#retrieve-the-last-health-check-log-entry)
  - [Test](#test)
    - [Create a New User](#create-a-new-user)
    - [Get All Users](#get-all-users)
    - [Delete a User by ID](#delete-a-user-by-id)
    - [Create a New Shop for a User](#create-a-new-shop-for-a-user)
    - [Get All Shops](#get-all-shops)
    - [Get a Specific Shop by ID](#get-a-specific-shop-by-id)
- [Definitions](#definitions)
- [License](#license)

## Introduction

The Spitfire Superadmin API is designed to provide various functionalities for managing shops, products, vendors, and more.

## Authentication

Authentication is required for certain endpoints. Please refer to the specific endpoint documentation for authentication details.

## API Endpoints

### Shop

#### Get Information from the Shop Endpoint

This endpoint retrieves information from the shop endpoint.

#### Get Information Related to All Shops

This endpoint retrieves information related to all shops in the system. Requires admin authentication.

#### Get Information Related to a Specific Shop

This endpoint retrieves information related to a specific shop identified by the provided shop ID. Requires admin authentication.

...

### Product

...

### Health

...

### Test

...

## Definitions

- [Shop](#shop)
- [Product](#product)
- [ShopsAndProducts](#shopsandproducts)
- [Error](#error)
- [Vendor](#vendor)

## License

This API is released under the MIT License.

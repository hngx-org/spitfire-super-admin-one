#!/usr/bin/env python3
"""API Template for the Shop-driven Operation"""

import os
import uuid
from flask import Blueprint, jsonify, request, abort, send_file
from super_admin_1 import db
from super_admin_1.models.shop import Shop
from super_admin_1.models.user import User
from super_admin_1.shop.shoplog_helpers import ShopLogs
from super_admin_1.models.product import Product
import os
from super_admin_1.models.shop_logs import ShopsLogs
from utils import admin_required


test = Blueprint("test", __name__, url_prefix="/api/admin/test")


# ============================== MY HELPER FUNCTON ================================
@test.route('/user/create', methods=['POST'])
#@admin_required(request)
def create_user():
    """Create a new user"""
    if not request.get_json():
        abort(400)
    data_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "section_order",
        "password",
        "is_verified",
        "two_factor_auth",
        "provider",
        "profile_pic",
        "refresh_token",
    ]
    for field in data_fields:
        if field not in request.get_json():
            abort(400)
    user = User(**request.get_json())
    db.session.add(user)
    db.session.commit()
    return jsonify(user.format()), 201


@test.route("/user/<user_id>/shop", methods=["POST"])
#@check_services_health
#@admin_required(request)
def create_shop(user_id):
    """Create a new shop"""
    if not request.get_json():
        abort(400)
    data_fields = ["name", "policy_confirmation", "reviewed", "rating"]
    for field in data_fields:
        if field not in request.get_json():
            abort(400)
        else:
            continue
    data = request.get_json()
    data["merchant_id"] = user_id
    shop = Shop(**data)
    db.session.add(shop)
    db.session.commit()

    """
  The following logs the action in the shop_log db
  """
    get_shop_id = shop.id
    action = ShopLogs(shop_id=get_shop_id, user_id=data["merchant_id"])
    action.log_shop_created()
    return jsonify(shop.format()), 201


@test.route('/shop/<shop_id>/product', methods=['POST'])
@admin_required(request=request)
def create_product(shop_id):
    """ Create a new product"""
    if not request.get_json():
        abort(400)

    data = request.get_json()
    data["shop_id"] = shop_id
    product = Product(**data)
    db.session.add(product)
    db.session.commit()

    return jsonify(product.format()), 201


# get request for shop
@test.route('/', methods=['GET'], strict_slashes=False, defaults={'shop_id': None})
@test.route('/<shop_id>', methods=['GET'])
@admin_required(request=request)
def get_shop(shop_id):
    """Get a shop or all shop"""
    if shop_id:
        return jsonify(Shop.query.filter_by(id=shop_id).first().format()), 200
    else:
        return jsonify([shop.format() for shop in Shop.query.all()]), 200


# Get request for user
@test.route("/user", methods=["GET"], strict_slashes=False, defaults={"user_id": None})
@test.route("/user/<user_id>", methods=["GET"])
@admin_required(request=request)
def get_user(user_id=None):
    """Get all users"""
    if user_id:
        return jsonify(User.query.filter_by(id=user_id).first().format()), 200
    else:
        return jsonify([user.format() for user in User.query.all()]), 200


# Delete user object
@test.route("/user/<user_id>", methods=["DELETE"])
@admin_required(request=request)
def delete_user(user_id):
    """Delete a user"""
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200


# Define a route to get all vendors, including all their details
@test.route("/all_vendors", methods=["GET"])
def get_all_vendors():
    try:
        # Retrieve all vendors from the database
        vendors = Shop.query.all()

        # Check if there are vendors to return
        if not vendors:
            return jsonify({"message": "No vendors found."}), 200

        # Prepare the list of vendors with all their details
        vendor_list = [vendor.format() for vendor in vendors]

        return jsonify({"vendors": vendor_list}), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})


# Define a route to temporarily delete a vendor
@test.route("/delete_vendor/<string:vendor_id>", methods=["DELETE"])
def temporarily_delete_vendor(vendor_id):
    try:
        # Check if the vendor_id is a valid UUID (assuming vendor IDs are UUIDs)
        if not is_valid_uuid(vendor_id):
            return jsonify({"error": "Invalid vendor ID format."}), 400

        # Find the vendor by ID and set their status to "temporary" deleted
        vendor = Shop.query.filter_by(id=vendor_id).first()
        if vendor:
            vendor.is_deleted = "temporary"
            db.session.commit()
            return (
                jsonify(
                    {
                        "status": "Success",
                        "message": "Vendor temporarily deleted successfully.",
                    }
                ),
                200,
            )
        else:
            return jsonify({"error": "Vendor not found."}), 404
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})


# Helper function to check if a string is a valid UUID
def is_valid_uuid(uuid_string):
    try:
        uuid.UUID(uuid_string, version=4)
        return True
    except ValueError:
        return False


# ======================================== HELPER FUNCTION END=============================================

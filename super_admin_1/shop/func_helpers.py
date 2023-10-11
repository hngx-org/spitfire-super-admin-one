#!/usr/bin/env pyhon3
"""API Temlate for the Shop driven Operation"""
from super_admin_1 import db
from flask import Blueprint, jsonify, request, abort, send_file
from super_admin_1.models.shop import Shop
from super_admin_1.models.user import User
from super_admin_1.models.shop_logs import ShopsLogs
from super_admin_1.shop.shoplog_helpers import ShopLogs
import os
from utils import super_admin_required
from health_check import check_services_health

test = Blueprint('test', __name__, url_prefix='/api/test')


# ============================== MY HELPER FUNCTON ================================
@test.route('/user/create', methods=['POST'])
@check_services_health
#@super_admin_required
def create_user():
    """ Create a new user"""
    if not request.get_json():
        abort(400)
    data_fields = ["username", "first_name", "last_name", "email", "section_order",
                   "password", "is_verified", "two_factor_auth", "provider", "profile_pic", "refresh_token"]
    for field in data_fields:
        if field not in request.get_json():
            abort(400)
    user = User(**request.get_json())
    db.session.add(user)
    db.session.commit()
    return jsonify(user.format()), 201


@test.route('/user/<user_id>/shop', methods=['POST'])
@check_services_health
#@super_admin_required
def create_shop(user_id):
    """ Create a new shop"""
    if not request.get_json():
        abort(400)
    data_fields = ["name", "policy_confirmation", "reviewed", "rating"]
    for field in data_fields:
        if field not in request.get_json():
            abort(400)
        else:
            continue
    data = request.get_json()
    data['merchant_id'] = user_id
    shop = Shop(**data)
    db.session.add(shop)
    db.session.commit()

    """
  The following logs the action in the shop_log db
  """
    get_shop_id = shop.id
    action = ShopLogs(
        shop_id=get_shop_id,
        user_id=data['merchant_id']
    )
    action.log_shop_created()
    return jsonify(shop.format()), 201


# get request for shop
@test.route('/', methods=['GET'], strict_slashes=False, defaults={'shop_id': None})
@test.route('/<shop_id>', methods=['GET'])
@check_services_health
#@super_admin_required
def get_shop(shop_id):
    """ Get a shop or all shop"""
    if shop_id:
        return jsonify(Shop.query.filter_by(id=shop_id).first().format()), 200
    else:
        return jsonify([shop.format() for shop in Shop.query.all()]), 200



# get request for user
@test.route('/user', methods=['GET'], strict_slashes=False, defaults={'user_id': None})
@test.route('/user/<user_id>', methods=['GET'])
#@super_admin_required
def get_user(user_id=None):
    """ Get all user"""
    if user_id:
        return jsonify(User.query.filter_by(id=user_id).first().format()), 200
    else:
        return jsonify([user.format() for user in User.query.all()]), 200


# delete user object
@test.route('/user/<user_id>', methods=['DELETE'])
@super_admin_required
def delete_user(user_id):
    """ Delete a user"""
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
# ======================================== HELPER FUNCTIN END=============================================



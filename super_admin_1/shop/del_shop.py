#!/usr/bin/env pyhon3
"""API Temlate for the Shop driven Operation"""
from super_admin_1 import db
from flask import Blueprint, jsonify, request, abort, send_file
from super_admin_1.models.shop import Shop
from super_admin_1.models.user import User
from super_admin_1.models.shop_logs import ShopsLogs
from super_admin_1.shop.shoplog_helpers import ShopLogs
import os

del_shop = Blueprint('del_shop', __name__, url_prefix='/api/shop')



@del_shop.route('/<shop_id>', methods=['PATCH'], strict_slashes=False)
def delete_shop(shop_id):
    """Delete a shop"""
    # verify if shop exists
    shop = Shop.query.filter_by(id=shop_id).first()
    if not shop:
        return jsonify({'forbidden': 'Shop not found'}), 404
    # check if shop is temporary
    if shop.is_deleted == 'temporary':
        return jsonify({'message': 'Shop already deleted'}), 400
    # delete shop temporarily
    shop.is_deleted = 'temporary'
    db.session.commit()

    """
    The following logs the action in the shop_log db
    """
    get_user_id = shop.user.id
    action = ShopLogs(
        shop_id=shop_id,
        user_id=get_user_id
    )
    action.log_shop_deleted(delete_type="temporary")
    return jsonify({'message': 'Shop temporarily deleted'}), 200


# ============================== MY HELPER FUNCTON ================================
@del_shop.route('/user/create', methods=['POST'])
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


@del_shop.route('/user/<user_id>/shop', methods=['POST'])
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
@del_shop.route('/', methods=['GET'], strict_slashes=False, defaults={'shop_id': None})
@del_shop.route('/<shop_id>', methods=['GET'])
def get_shop(shop_id):
    """ Get a shop or all shop"""
    if shop_id:
        return jsonify(Shop.query.filter_by(id=shop_id).first().format()), 200
    else:
        return jsonify([shop.format() for shop in Shop.query.all()]), 200


# delete shop object permanently out of the DB
@del_shop.route('/<shop_id>/del', methods=['DELETE'])
def perm_del(shop_id):
    """ Delete a shop"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if not shop:
        abort(404)
    db.session.delete(shop)
    db.session.commit()
    return jsonify({'message': 'Shop deleted aggresively'}), 200


# get request for user
@del_shop.route('/user', methods=['GET'], strict_slashes=False, defaults={'user_id': None})
@del_shop.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """ Get all user"""
    if user_id:
        return jsonify(User.query.filter_by(id=user_id).first().format()), 200
    else:
        return jsonify([user.format() for user in User.query.all()]), 200

# delete user object


@del_shop.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Delete a user"""
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
# ======================================== HELPER FUNCTIN END=============================================


@del_shop.route("/logs/shops", defaults={"shop_id": None})
@del_shop.route("/logs/shops/<int:shop_id>")
def get_all_shop_logs(shop_id):
    """Get all shop logs"""
    if not shop_id:
        return (
            jsonify(
                {
                    "message": "success",
                    "logs": [
                        log.format() if log else [] for log in ShopsLogs.query.all()
                    ],
                }
            ),
            200,
        )

    return (
        jsonify(
            {
                "message": "success",
                "logs": [
                    log.format() if log else []
                    for log in ShopsLogs.query.filter_by(shop_id=shop_id).all()
                ],
            }
        ),
        200,
    )


@del_shop.route("/logs/shops/download", defaults={"shop_id": None})
@del_shop.route("/logs/shops/<int:shop_id>/download")
def download_shop_logs(shop_id):
    """Download all shop logs"""
    logs = []
    if not shop_id:
        logs = [log.format() if log else [] for log in ShopsLogs.query.all()]
    else:
        logs = [
            log.format() if log else []
            for log in ShopsLogs.query.filter_by(shop_id=shop_id).all()
        ]
    # Create a temporary file to store the strings
    temp_file_path = f"{os.path.abspath('.')}/temp_file.txt"
    with open(temp_file_path, "w") as temp_file:
        temp_file.write("\n".join(logs))

    response = send_file(
        temp_file_path, as_attachment=True, download_name="shoplogs.txt"
    )
    os.remove(temp_file_path)

    return response

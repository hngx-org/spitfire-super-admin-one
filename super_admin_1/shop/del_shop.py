#!/usr/bin/env pyhon3
"""API Temlate for the Shop driven Operation"""

from super_admin_1 import db
from flask import Blueprint, jsonify, request, abort
from super_admin_1.models.shop import Shop
from super_admin_1.models.user import User

del_shop = Blueprint('del_shop', __name__)


@del_shop.route('/shop/<shop_id>', methods=['DELETE'])
def delete_shop(shop_id):
  """Delete a shop"""
  # verify json data
  data = request.get_json()
  print(data)
  if not request.is_json:
    abort(400), 'JSON data required'
  # verify if shop exists
  shop = Shop.query.filter_by(id=shop_id).first()
  if not shop:
    abort(404), 'Invalid shop'
  # change object attribute is_delete from active to temporary
  shop.is_deleted = 'temporary'
  # save object to the database
  shop.update()  
  # send message of operation
  return jsonify({'message': 'Shop temorary deleted'})


@del_shop.route('/user/create', methods=['POST'])
def create_user():
  if not request.get_json():
    abort(400)
  data_fields = ["username", "first_name", "last_name", "email", "section_order", "password", "is_verified", "two_factor_auth", "provider", "profile_pic", "refresh_token"]
  for field in data_fields:
    if field not in request.get_json():
      abort(400)
  user = User(**request.get_json())
  db.session.add(user)
  db.session.commit()
  return jsonify(user.format()), 201


@del_shop.route('/user/<user_id>/shop', methods=['POST'])
def create_shop(user_id):
  """ Createa new shop"""
  if not request.get_json():
    abort(400)
  print("hI")
  data_fields = ["name", "policy_confimation", "reviewed", "rating"]
  for field in data_fields:
    if field not in request.get_json():
      abort(400)
    else:
      continue
  data = request.get_json()
  print("HI: ", data)
  data['merchant_id'] = user_id
  shop = Shop(**data)
  db.session.add(shop)
  db.session.commit()
  return jsonify(shop.format()), 201


# get request for shop
@del_shop.route('/shop', methods=['GET'], strict_slashes=False, defaults={'shop_id': None})
@del_shop.route('/shop/<shop_id>', methods=['GET'])
def get_shop(shop_id):
  """ Get a shop"""
  if shop_id:
    return jsonify(Shop.query.filter_by(id=shop_id).first().format()), 200
  else:
    return jsonify([shop.format() for shop in Shop.query.all()]), 200
  
  
# delete shop object
# @del_shop.route('/shop/<shop_id>', methods=['DELETE'])
# def perm_del(shop_id):
#   """ Delete a shop"""
#   shop = Shop.query.filter_by(id=shop_id).first()
#   if not shop:
#     abort(404)
#   db.session.delete(shop)
#   db.session.commit()
#   return jsonify({'message': 'Shop deleted'}), 200


# get request for user
@del_shop.route('/user/<user_id>/shop', methods=['GET'])
def get_shops(user_id):
  """ Get all shops"""
  user = User.query.filter_by(id=user_id).first()
  return jsonify([shop.format() for shop in user.shops]), 200

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



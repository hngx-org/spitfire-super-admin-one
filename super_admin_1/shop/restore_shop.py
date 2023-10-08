"""api template for the shop driven operation"""

from super_admin_1 import db
from flask import Blueprint, jsonify, request, abort
from super_admin_1.models.shop import Shop
from super_admin_1.models import User

restore_shop = Blueprint("restore_shop", __name__)


@restore_shop.route("/shop/<shop_id>", methods=["PATCH"])
def restore_shop(shop_id):
    """restores a deleted shop by setting their "temporary" to "active" fields
    Args:
        shop_id (string)
    returns:
        JSON response with status code and message:
        -success(HTTP 200):shop restored successfully
        -success(HTTP 200): if the shop with provided not marked as deleted
    """
    data = request.get_json()
    if not request.is_json:
        abort(400), "JSON data required"
    shop = shop.query.filter_by(id=shop_id).first()
    if not shop:
        abort(404), "Invalid shop"
    # change the object attribute from temporary to active
    if shop.is_deleted == "temporary":
        shop.is_deleted = "active"
        db.session.commit()
        return jsonify({"message": "shop restored sufccessfully"}), 200
    else:
        return jsonify({"message": "shop is not marked as deleted"}), 200

"""api template for the shop driven operation"""

from flask import Blueprint, jsonify, request, abort
from super_admin_1.models.shop import Shop
from super_admin_1.models.alternative import Database as db
from super_admin_1.shop.shoplog_helpers import ShopLogs
from utils import super_admin_required

restore_shop_bp = Blueprint(
    "restore_shop", __name__, url_prefix="/api/restore_shop")


@restore_shop_bp.route("/<shop_id>", methods=["PATCH"])
@super_admin_required
def restore_shop(shop_id):
    """restores a deleted shop by setting their "temporary" to "active" fields
    Args:
        shop_id (string)
    returns:
        JSON response with status code and message:
        -success(HTTP 200):shop restored successfully
        -success(HTTP 200): if the shop with provided not marked as deleted
    """
    # data = request.get_json()
    # if not request.is_json:
    # abort(400), "JSON data required"
    shop = Shop.query.filter_by(id=shop_id).first()
    if not shop:
        abort(404), "Invalid shop"
    # change the object attribute from temporary to active
    if shop.is_deleted == "temporary":
        shop.is_deleted = "active"
        try:
            db.session.commit()

            """
            The following logs the action in the shop_log db
            """
            get_user_id = shop.user.id
            action = ShopLogs(
                shop_id=shop_id,
                user_id=get_user_id
            )
            action.log_shop_deleted(delete_type="active")

            return jsonify({"message": "shop restored successfully"}), 200
        except Exception as e:
            db.session.rollback()
            abort(500, f"Failed to restore shop: {str(e)}")
    else:
        return jsonify({"message": "shop is not marked as deleted"}), 200

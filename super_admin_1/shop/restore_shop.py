"""api template for the shop driven operation"""

from flask import Blueprint, jsonify, request, abort
from super_admin_1.models.shop import Shop
from super_admin_1.models.alternative import Database as db
from flask_login import login_required


restore_shop = Blueprint("restore_shop", __name__, url_prefix='/api/restore_shop')


@restore_shop.route("/<shop_id>", methods=["PATCH"])
@login_required
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
    #if not request.is_json:
        #abort(400), "JSON data required"
    shop = Shop.query.filter_by(id=shop_id).first()
    if not shop:
        abort(404), "Invalid shop"
    # change the object attribute from temporary to active
    if shop.is_deleted == 'temporary':
        shop.is_deleted = 'active'
        try:
            db.session.commit()
            return jsonify({"message": "shop restored sufccessfully"}), 200
        except Exception as e:
            db.session.rollback()
            abort(500, f'Failed to restore shop: {str(e)}')   
    else:
        return jsonify({"message": "shop is not marked as deleted"}), 200

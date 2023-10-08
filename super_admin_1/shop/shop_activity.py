from super_admin_1 import db
from flask import Blueprint, jsonify
from super_admin_1.models.shop_log import ShopLog


shop_activity = Blueprint('shop_activity', __name__)


@shop_activity.route('/shop/actions', methods=['GET'])
def shop_actions():
    data = ShopLog.query.all()
    return jsonify([action.format() for action in data]), 200


# The following lines of code needs to by added to actions that needs to be logged
# get_user_id = shop.user.id
# notice = {"user_id": get_user_id,
#             "action": "delete shop", "shop_id": shop_id}

# activity = ShopLog(**notice)
# activity.insert()

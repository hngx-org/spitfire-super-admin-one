from super_admin_1 import db
from flask import Blueprint, jsonify
from super_admin_1.models.shop_logs import ShopsLogs


events = Blueprint("events", __name__, url_prefix="/api/events")


@events.route('/shop/actions', methods=['GET'])
def shop_actions():
    data = ShopsLogs.query.all()
    return jsonify([action.format_json() for action in data]), 200

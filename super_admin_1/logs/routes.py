import os
from datetime import date
from utils import super_admin_required
from flask import Blueprint, jsonify, send_file
from super_admin_1.models.shop_logs import ShopsLogs
from super_admin_1.logs.product_action_logger import generate_log_file_d, logger


logs = Blueprint("logs", __name__, url_prefix="/api/logs")


@logs.route("/shops", defaults={"shop_id": None})
@logs.route("/shops/<shop_id>")
@super_admin_required
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

@logs.route("/shops/download", defaults={"shop_id": None})
@logs.route("/shops/<shop_id>/download")
@super_admin_required
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

@logs.route("/shop/actions", methods=["GET"])
@super_admin_required
def shop_actions():
    data = ShopsLogs.query.all()
    return jsonify([action.format_json() for action in data]), 200

@logs.route("/product/download")
# @super_admin_required
def log():
    """Download product logs"""
    try:
        filename = generate_log_file_d()
        if filename is False:
            return {
                "message": "No log entry exists"
            }, 200
        path = os.path.abspath(filename)
        return send_file(path), 200
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
        return jsonify(
            {
                "message": "Could not download audit logs",
                "error": f"{error.__doc__}"
            }
        ), 500


@logs.route("/server/download")
def server_log():
    """Download server logs"""
    try:
        filename = f'logs/server_logs_{date.today().strftime("%Y_%m_%d")}.log'
        if filename is False:
            return {
                "message": "No log entry exists"
            }, 204
        path = os.path.abspath(filename)
        return send_file(path), 200
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
        return jsonify(
            {
                "message": "Could not download server logs",
                "error": f"{error}"
            }
        ), 500

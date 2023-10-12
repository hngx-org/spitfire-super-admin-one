"""Endpoint to test notification capability"""
from flask import Blueprint, request, jsonify
from super_admin_1.notification.notification_helper import notify, notify_test
from super_admin_1.logs.product_action_logger import logger

notification = Blueprint('notification', __name__, url_prefix='/api/notification')

@notification.route("/", methods=["POST"])
def test_notification():
    """send a mail to a user"""
    acceptable_keys = ["vendor_id", "product_id", "shop_id", "reason", "action"]
    try:
        data = request.get_json()
        if len(data.keys()) > 4:
            return jsonify(
                {
                    "message": "Too many keys",
                    "error": "Unnecessary key-value pair present"
                }
            ), 400
        for key in data.keys():
            if key not in acceptable_keys:
                return jsonify(
                    {
                        "message": "Invalid key",
                        "error": f"{key} is not a valid key"
                    }
                ), 400
        if "product_id" in data.keys() and "shop_id" in data.keys():
            return jsonify(
                {
                    "message": "Bad Request",
                    "error": "product_id and shop_id cannot co-exist"
                }
            ), 400

        # response = notify(data.get("vendor_id"), data.get("action"), **data)
        response = notify_test("Wonderful", "adeonederful20@gmail.com")
        print(f"response: {response}")
        if response.get("success") is False:
            return jsonify(
                {
                    "message": "Email not sent",
                    "error": "messaging service is down"
                }
            ), 200
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
        return jsonify(
            {
                "message": "an error occured during execution, try again",
                "error": f"{type(error).__name__}"
            }
        ), 500
    
    return jsonify(
        {
            "message": "Email sent successfully",
            "data": response.get("data", None)

        }
    )

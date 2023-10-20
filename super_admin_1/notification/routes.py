"""Endpoint to test notification capability"""
from flask import Blueprint, request, jsonify
from super_admin_1.notification.notification_helper import  notify_test
from super_admin_1.logs.product_action_logger import logger

notification = Blueprint('notification', __name__, url_prefix='/api/admin/notification')

@notification.route("/", methods=["POST"])
def test_notification():
    """send a mail to a user"""
    acceptable_keys = ["product_id", "shop_id", "reason", "action", "email"]
    acceptable_actions = ["ban", "unban", "sanction", "unsanction", "deletion"]
    try:
        data = request.get_json()
        action = data.get("action")
        if len(data.keys()) > 3:
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
        if action not in acceptable_actions:
            return jsonify(
                {
                    "message": "Invalid action",
                    "error": f"{action} is not a valid action"
                }
            ), 400
        if "product_id" in data.keys() and "shop_id" in data.keys():
            return jsonify(
                {
                    "message": "Bad Request",
                    "error": "product_id and shop_id cannot co-exist"
                }
            ), 400

        # response = notify(action=action, **data)
        if not (data.get("product_id", None)):
            response = notify_test(action=action, email=data.get("email"),
                                shop_id=data.get("shop_id"))
        else:
            response = notify_test(action=action, email=data.get("email"),
                                product_id=data.get("product_id"))
        print(f"response: {response}")
        if not response.get("success", None):
            return jsonify(response)
        if response.get("success") is False:
            return jsonify(
                {
                    "message": "Email not sent",
                    "error": "messaging service is down"
                }
            ), 424
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

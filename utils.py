from functools import wraps
from flask import request, jsonify, json
from super_admin_1.errors.handlers import CustomError
import requests

def super_admin_required(func):
    @wraps(func)
    def get_user_role(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Unauthorized", "message": "You are not logged in"}), 401
        
        api_url = 'https://auth.akuya.tech/api/get-auth'
        response = requests.post(api_url, json={"token": auth_header, "role": "super_admin_1"})

        if response.status_code != 200:
            return jsonify({"error": "Unauthorized", "message": "Unable to fetch user role"}), 401

        user_data = response.json()

        if not user_data.get("authorized"):
            return jsonify({"error": "Unauthorized", "message": "Super-admin access required"}), 403

        return jsonify({"status": 200, "msg": "authorized", "id": user_data.get("id")})
    
    return get_user_role


def raise_validation_error(error):
    msg = []
    for err in error.errors():
        msg.append({
            "field": err["loc"][0],
            "error":err["msg"]
        })
    raise CustomError("Bad Request",400,msg)
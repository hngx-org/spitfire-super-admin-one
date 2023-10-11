from functools import wraps
from flask import request, jsonify, json
import requests

def super_admin_required(func):
    @wraps(func)
    def get_user_role(*args, **kwargs):
        auth_url = 'https://auth.akuya.tech/api/authorize'
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Unauthorized", "message": "You are not logged in"}), 401
        if auth_header.startswith("Bearer"):
            token = auth_header.split(" ")[1]
            print(token)
        
        response = requests.post(
            auth_url, 
            {
                "token": token, 
                "role": "admin"
                }
            )

        if response.status_code != 200:
            return jsonify({"error": "Unauthorized", "message": "Unable to fetch user role"}), 401

        if not user_data.get("authorized"):
            return jsonify({"error": "Unauthorized", "message": "Super-admin access required"}), 403
        
        user_data = response.json()
        user_id = user_data.get("user")["id"]


        return func(user_id, *args, **kwargs)
    
    return get_user_role

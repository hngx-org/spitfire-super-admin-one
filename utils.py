from functools import wraps
from super_admin_1.errors.handlers import Unauthorized, Forbidden, CustomError
from flask import request
import requests
import requests


def super_admin_required(func):
    @wraps(func)
    def get_user_role(user_id, product_id, *args, **kwargs):
        auth_url = "https://auth.akuya.tech/api/authorize"
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise CustomError(error="Unauthorized", code=401,  message="You are not logged in")
        token = None
        if auth_header.startswith("Bearer"):
            token = auth_header.split(" ")[1]
            print(token)

        response = requests.post(
            auth_url,
            {
                "token": token,
                "role": "admin",
            },
        )

        if response.status_code != 200:
            raise CustomError(error="Bad Request", code=400,  message="Something went wrong while Authenticating this User")

        user_data = response.json()

        if not user_data.get("authorized"):
            raise CustomError(error="Forbidden", code=403,  message="No Permissions to access the requested resource")

        user_id = user_data.get("user")["id"]

        return func(user_id, product_id, *args, **kwargs)

    return get_user_role

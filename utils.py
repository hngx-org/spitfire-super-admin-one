from functools import wraps
from super_admin_1.errors.handlers import Unauthorized, Forbidden, CustomError
from flask import request
import requests


def super_admin_required(func):
    @wraps(func)
    def get_user_role( *args, **kwargs):
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
            print(response)
            raise CustomError(error="Bad Request", code=400,  message="Something went wrong while Authenticating this User")

        user_data = response.json()

        if not user_data.get("authorized"):
            raise CustomError(error="Forbidden", code=403,  message="No Permissions to access the requested resource")

        user_id = user_data.get("user")["id"]

        return func(user_id,  *args, **kwargs)

    return get_user_role


def raise_validation_error(error):
    msg = []
    for err in error.errors():
        msg.append({
            "field": err["loc"][0],
            "error":err["msg"]
        })
    raise CustomError("Bad Request",400,msg)

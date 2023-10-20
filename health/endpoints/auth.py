import os

from health import USER_ID

NAME = "Authentication"
BASE_URL = "https://staging.zuri.team/api/auth"

USER = {
    "firstName": "Health Check",
    "lastName": "Super Admin",
    "email": "zuri-health-check@gmail.com",
    "password": "zuri-health-check123",
}

ENDPOINTS_CONFIG = [
    # {
    #     "url": "/api/auth/signup",
    #     "method": "POST",
    #     "body_params": USER,
    # },
    {
        "url": "/api/auth/check-email",
        "method": "POST",
        "body_params": {
            "email": USER["email"]
        },
    },
    {
        "url": "/api/auth/verify/{token}",
        "method": "GET",
        "path_params": {
            "token": os.getenv("ACCESS_TOKEN")
        },
    },
    {
        "url": "/api/auth/verify/resend",
        "method": "POST",
        "body_params": {
            "email": USER["email"]
        },
    },
    {
        "url": "/api/auth/login",
        "method": "POST",
        "body_params": {
            "email": USER["email"],
            "password": USER["password"]
        },
    },
    {
        "url": "/api/auth/reset-password",
        "method": "POST",
        "body_params": {
            "email": USER["email"]
        },
    },
    # {
    #     "url": "/api/auth/reset-password",
    #     "method": "PATCH",
    #     "body_params": {
    #         "token": "",
    #         "password": USER["password"]
    #     },
    #     "auth_required": True,
    # },
    {
        "url": "/api/auth/2fa/enable",
        "method": "POST",
        "body_params": {
            "email": USER["email"],
        },
        "auth_required": True,
    },
    # {
    #     "url": "/api/auth/2fa/send-code",
    #     "method": "POST",
    #     "body_params": {
    #         "email": USER["email"],
    #     },
    # },
    # {
    #     "url": '/api/auth/2fa/verify-code',
    #     "method": "POST",
    #     "body_params": {
    #         "token": "",
    #         "email": USER["email"],
    #     },
    # },
    {
        "url": "/api/authorize/roles",
        "method": "GET",
        "auth_required": True,
    },
    {
        "url": "/api/authorize",
        "method": "POST",
        "body_params": {
            "token": os.getenv("ACCESS_TOKEN"),
            "permission": "product.read",
        },
    },
    {
        'url': '/api/authorize/permissions',
        'method': 'GET',
    },
    {
        "url": "/users/permission",
        "method": "POST",
        "body_params": {
            "userId": USER_ID,
            "permissionId": "product.read",
        },
        "auth_required": True,
    },
    {
        "url": "/users/permission",
        "method": "DELETE",
        "body_params": {
            "userId": USER_ID,
            "permissionId": "product.read",
        },
        "auth_required": True,
    },
    {
        "url": "/users/{user_id}/role",
        "method": "PUT",
        "body_params": {
            "roleId": 3,
            "roleName": "admin",
        },
        "path_params": {
            "user_id": USER_ID,
        },
        "auth_required": True,
    },
    {
        "url": "/users",
        "method": "GET",
        "auth_required": True,
    },
    {
        "url": "/auth/change-email",
        "method": "PATCH",
        "body_params": {
            "newEmail": "health-check@zuri.team",
        },
        "auth_required": True,
    }
]

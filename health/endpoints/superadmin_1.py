
BASE_URL = "https://staging.zuri.team/api/v1/admin"
NAME = "SUPERADMIN 1"
SHOP_ID = "c5ae1c3f-4578-43c3-b1d5-76d315053340"#"6e07533a-b806-4b1e-be10-fad03978eac8"
PRODUCT_ID = "69cf1ea7-4209-4d62-b7d7-3f63a0753bf4" #make sure it's valid

ENDPOINTS_CONFIG = [
    {
        "url": "/shops/all",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True 
    },

    {
        "url": "/shops/endpoint",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True  
    },

    {
        "url": "/shops/{shop_id}",
        "method": "GET",
        "path_params": {
            "shop_id": f"{SHOP_ID}" 
        },
        "body_params": None,
        "auth_required": True  
    },

    {
        "url": "/shops/{shop_id}/ban",
        "method": "PUT",
        "path_params": {"shop_id": f"{SHOP_ID}"},
        "body_params": {"reason": "Breaking the rules"},
        "auth_required": True
    },

    # {
    #     "url": "/shop/banned_vendors",
    #     "method": "GET",
    #     "auth_required": True
    # },

    {
        "url": "/shops/{shop_id}/unban",
        "method": "PUT",
        "path_params": {"shop_id": f"{SHOP_ID}"},
        "auth_required": True
    },

    {
        "url": "/shops/{shop_id}/soft-delete",
        "method": "PATCH",
        "path_params": {"shop_id": f"{SHOP_ID}"},
        "body_params": {"reason": "Shop is selling illegal products"},
        "auth_required": True
    },

    # {
    #     "url": "/shop/temporarily_deleted_vendors",
    #     "method": "GET",
    #     "auth_required": True
    # },

    {
        "url": "/shops/{shop_id}/restore",
        "method": "PATCH",
        "path_params": {"shop_id": f"{SHOP_ID}"},
        "auth_required": True
    },

    # {
        # "url": "/api/admin/delete_shop/{shop_id}",
        # "method": "DELETE",
        # "path_params": {"shop_id": f"{shop_id}"},
        # "auth_required": True
    # },

    # #NOT USED
    # {
    #     "url": "/shops/sanctioned",
    #     "method": "GET",
    #     "auth_required": True
    # },

    #PRODUCT ENDPOINTS
    {
        "url": "/products/all",
        "method": "GET",
        "auth_required": True
    },
    {
        "url": "/products/pending/all",
        "method": "GET",
        "auth_required": True
    },

    {
        "url": "/products/{product_id}",
        "method": "GET",
        "path_params": {
            "product_id": f"{PRODUCT_ID}"
        },
        "auth_required": True
    },

    {
    "url": "/products/{product_id}/sanction",
    "method": "PATCH",
    "path_params": {
        "product_id": f"{PRODUCT_ID}"
    },
    "body_params": None,
    "auth_required": True
    },
    {
    "url": "/products/products-statistics",
    "method": "GET",
    "body_params": None,
    "auth_required": True
    },

    {
        "url": "/products/{product_id}/soft-delete",
        "method": "DELETE",
        "path_params": {
            "product_id": f"{PRODUCT_ID}"
        },
        "body_params": None,
        "auth_required": True
    },

    {
        "url": "/products/{product_id}/restore",
        "method": "PATCH",
        "path_params": {
            "product_id": f"{PRODUCT_ID}"
        },
        "auth_required": True
    },

    # {
    #     "url": "/product/temporarily_deleted_products",
    #     "method": "GET",
    #     "auth_required": True
    # },

    {
        "url": "/products/{product_id}/approve",
        "method": "PATCH",
        "path_params": {
            "product_id": f"{PRODUCT_ID}"
        },
        "auth_required": True
    },

    {
        "url": "/products/{product_id}",
        "method": "DELETE",
        "path_params": {
            "product_id": f"{PRODUCT_ID}"
        },
        "body_params": None,
        "auth_required": True
    },

    # NOTIFICATION ENDPOINTS
    {
        "url": "/notifications/",
        "method": "POST",
        "body_params":{
            "product_id": "fb75dd22-0a10-4f44-9b75-a742578471b2",
            "email": "zurihealthcheck@gmail.com",
            "action": "deletion"
        },
    }


]

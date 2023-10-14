
BASE_URL = "https://spitfire-superadmin-1.onrender.com"
NAME = "SUPERADMIN 1"
SHOP_ID = "4ed444e0-1005-4fb7-9f9b-a01de39890fc"
PRODUCT_ID = "d7955c27-4d71-4cd6-a6bb-e6402151d51f"

ENDPOINTS_CONFIG = [
    {
        "url": "/api/admin/shop/all",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True 
    },

    {
        "url": "/api/admin/shop/endpoint",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True  
    },

    {
        "url": "/api/admin/shop/{shop_id}",
        "method": "GET",
        "path_params": {
            "shop_id": f"{SHOP_ID}" 
        },
        "body_params": None,
        "auth_required": True  
    },

    {
        "url": "/api/admin/shop/ban_vendor/{shop_id}",
        "method": "PUT",
        "path_params": {"shop_id": f"{SHOP_ID}"},
        "body_params": {"reason": "Breaking the rules"},
        "auth_required": True
    },

    {
        "url": "/api/admin/shop/banned_vendors",
        "method": "GET",
        "auth_required": True
    },

    {
        "url": "/api/admin/shop/unban_vendor/{shop_id}",
        "method": "PUT",
        "path_params": {"shop_id": f"{SHOP_ID}"},
        "auth_required": True
    },

    # {
    #     "url": "/api/admin/shop/delete_shop/{shop_id}",
    #     "method": "PATCH",
    #     "path_params": {"shop_id": f"{SHOP_ID}"},
    #     "body_params": {"reason": "Shop is selling illegal products"},
    #     "auth_required": True
    # },

    {
        "url": "/api/admin/shop/temporarily_deleted_vendors",
        "method": "GET",
        "auth_required": True
    },

    {
        "url": "/api/admin/shop/restore_shop/{shop_id}",
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

    {
        "url": "/api/admin/shop/sanctioned",
        "method": "GET",
        "auth_required": True
    },

    #PRODUCT ENDPOINTS
    {
        "url": "/api/admin/product/all",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },

    {
        "url": "/api/admin/product/{product_id}",
        "method": "GET",
        "path_params": {
            "product_id": f"{PRODUCT_ID}"
        },
        "body_params": None,
        "auth_required": True
    },

    {
        "url": "/api/admin/product/{product_id}",
        "method": "GET",
        "path_params": {
            "product_id": f"{PRODUCT_ID}"
        },
        "body_params": None,
        "auth_required": True
    },

    # {
    # "url": "/api/admin/product/sanction/{product_id}",
    # "method": "PATCH",
    # "path_params": {
    #     "product_id": f"{PRODUCT_ID}"
    # },
    # "body_params": None,
    # "auth_required": True
    # },

    {
        "url": "/api/admin/product/restore/{product_id}",
        "method": "PATCH",
        "path_params": {
            "product_id": f"{PRODUCT_ID}"
        },
        "body_params": None,
        "auth_required": True
    },

    # {
    #     "url": "/api/admin/product/delete/{product_id}",
    #     "method": "PATCH",
    #     "path_params": {
    #         "product_id": f"{PRODUCT_ID}"
    #     },
    #     "body_params": None,
    #     "auth_required": True
    # },

    {
        "url": "/api/admin/product/approve/{product_id}",
        "method": "PATCH",
        "path_params": {
            "product_id": f"{PRODUCT_ID}"
        },
        "body_params":  None,
        "auth_required": True
    },

    {
        "url": "/api/admin/product/temporarily_deleted_products",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },


    # {
    #     "url": "/api/admin/product/delete/{product_id}",
    #     "method": "DELETE",
    #     "path_params": {
    #         "product_id": f"{PRODUCT_ID}"
    #     },
    #     "body_params": None,
    #     "auth_required": True
    # },

    # NOTIFICATION ENDPOINTS
    {
        "url": "/api/admin/notification/",
        "method": "POST",
        "body_params":{
            "product_id": "fb75dd22-0a10-4f44-9b75-a742578471b2",
            "email": "farimomoh@gmail.com",
            "action": "deletion"
        },
        "auth_required": False
    }


]

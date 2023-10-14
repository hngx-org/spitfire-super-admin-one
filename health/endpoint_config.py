shop_id = "4ed444e0-1005-4fb7-9f9b-a01de39890fc"

ENDPOINTS_CONFIG = {
        "get_all_shops": {
        "url": "/api/admin/shop/all",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True 
    },

    "shop_endpoint": {
    "url": "/api/admin/shop/endpoint",
    "method": "GET",
    "path_params": None,
    "body_params": None,
    "auth_required": True  
    },

    "get_shop": {
    "url": "/api/admin/shop/{shop_id}",
    "method": "GET",
    "path_params": {
        "shop_id": f"{shop_id}" 
    },
    "body_params": None,
    "auth_required": True  
    },

    "ban_vendor":{
        "url": "/api/admin/shop/ban_vendor/{shop_id}",
        "method": "PUT",
        "path_params": {"shop_id": f"{shop_id}"},
        "body_params": {"reason": "Breaking the rules"},
        "auth_required": True
    },

    "all_banned_vendor":{
    "url": "/api/admin/shop/banned_vendors",
    "method": "GET",
    "auth_required": True
    },

    "unban_vendor":{
    "url": "/api/admin/shop/unban_vendor/{shop_id}",
    "method": "PUT",
    "path_params": {"shop_id": f"{shop_id}"},
    "auth_required": True
    },

    "temporary_delete_vendor": {
    "url": "/api/admin/shop/delete_shop/{shop_id}",
    "method": "PATCH",
    "path_params": {"shop_id": f"{shop_id}"},
    "body_params": {"reason": "Shop is selling illegal products"},
    "auth_required": True
    },

    "all_temporary_delete_vendor":{
    "url": "/api/admin/shop/temporarily_deleted_vendors",
    "method": "GET",
    "auth_required": True
    },

    "restore_deleted_vendor":{
    "url": "/api/admin/shop/restore_shop/{shop_id}",
    "method": "PATCH",
    "path_params": {"shop_id": f"{shop_id}"},
    "auth_required": True
    },

    # "permanent_delete_vendor":{
    # "url": "/api/admin/delete_shop/{shop_id}",
    # "method": "DELETE",
    # "path_params": {"shop_id": f"{shop_id}"},
    # "auth_required": True
    # },

    "sanctioned_shop": {
        "url": "/api/admin/shop/sanctioned",
        "method": "GET",
        "auth_required": True
    }
    


}

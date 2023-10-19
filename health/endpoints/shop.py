BASE_URL = "https://zuriportfolio-shop-internal-api.onrender.com"
NAME = "SHOP"
PRODUCT_NAME = "Zuri Chat"
PRODUCT_ID = "dced1529-c998-492c-aa6a-0a57707989a5"
SHOP_ID = "013649dc-5957-479a-b173-25e61416e2f5"
ORDER_ID = "0103c7c3-0026-431a-a2fa-5e4a029c3e12"
PRODUCT_DRAFT = {
    "image": bytes("https://zuri.chat/static/media/logo.36d2d48a.svg", 'utf-8'),
    "shopId": SHOP_ID,
    "category_id": "Health & Fitness",
    "name": "Zuri Chat",
    "description": "Zuri Chat is a messaging app built for teams",
    "quantity": 100,
    "price": 1000,
    "discountPrice": 900,
    "tax": 100,
    "currency": "USD",
    "assets_name": "Zuri Chat",
    "assets_link": "https://zuri.chat/static/media/logo.36d2d48a.svg",
    "assets_note": "Zuri Chat is a messaging app built for teams",
    "assets_type": "image",
}

PRODUCT_CATEGORY_DRAFT = {
    "name": "Zuri Tester Category",
    "parent_id": None
}
DISCOUNT_DRAFT = {
    "discount_type": "string",
    "amount": 0,
    "quantity": 1,
    "maximum_discount_price": 0,
    "product_ids": [
        "valid-uuid"
    ],
    "valid_from": "2023-10-16T17:51:57.337Z",
    "valid_to": "2023-10-16T17:51:57.337Z"
}

SHOP_DRAFT = {
    "name": "Zuri Test Shop",
}

ENDPOINTS_CONFIG = [

    # Fetch all products
    {
        "url": "/api/products",
        "method": "GET",
        "auth_required": True
    },
    
    #Fetch all marketplace products
    {
        "url": "/api/products/marketplace",
        "method": "GET",
    },

    #Create a product
    # {
    #     "url": "/api/product/add",
    #     "method": "POST",
    #     "body_params": PRODUCT_DRAFT,
    #     "headers": {"Content-Type": "multipart/form-data"},
    #     "is_form_data": True,
    #     "auth_required": True
    # },

    #Delete product by id
    # {
    #     "url": "/api/product/{product_id}",
    #     "method": "DELETE",
    #     "path_params": {"product_id": "1"},
    #     "body_params": None,
    #     "query_params": None,
    #     "auth_required": True
    # },

    #Create a product Category
    {
        "url": "/api/product/category",
        "method": "POST",
        "body_params": PRODUCT_CATEGORY_DRAFT,
        "auth_required": True
    },

    #Retrieve product categories
    {
        "url": "/api/product/categories",
        "method": "GET",
    },

    #Fetch product by id
    {
        "url": "/api/product/{product_id}",
        "method": "GET",
        "path_params": {"product_id": PRODUCT_ID},
    },
    

    # Upload product assets
    {
        "url": "/api/product/assets/{product_id}",
        "method": "PATCH",
        "path_params": {"product_id": PRODUCT_ID},
        "body_params": {
            "name": "Nike Wears",
            "link": "https://benrobo.co",
            "notes": "some notes",
            "type": "external"
        },
        "auth_required": True
    },
    # Upload new product image
    {
        "url": "/api/product/{product_id}/image",
        "method": "POST",
        "path_params": {"product_id": PRODUCT_ID},
        "body_params": {
            "image": bytes("https://zuri.chat/static/media/logo.36d2d48a.svg", 'utf-8'),
        },
        "headers": {"Content-Type": "multipart/form-data"},
        "is_form_data": True,
        "auth_required": True
    },

    #Get product assets
    {
        "url": "/api/product/{product_id}/assets",
        "method": "GET",
        "path_params": {"product_id": PRODUCT_ID},
    },
    #Get product images
    {
        "url": "/api/product/{product_id}/image",
        "method": "GET",
        "path_params": {"product_id": PRODUCT_ID},
    },

    #Update product image
    {
        "url": "/api/product/{product_id}/image/{image_id}",
        "method": "PATCH",
        "path_params": {
            "product_id": PRODUCT_ID,
            "image_id": 115
        },
        "body_params": {
            "image": bytes("https://zuri.chat/static/media/logo.36d2d48a.svg", 'utf-8'),
        },
        "headers": {"Content-Type": "multipart/form-data"},
        "auth_required": True
    },
    
    # #Delete product image
    # {
    #     "url": "/api/product/{product_id}/image/{image_id}",
    #     "method": "DELETE",
    #     "path_params": {
    #         "product_id": PRODUCT_ID,
    #         "image_id": 115
    #     },
    #     "auth_required": True
    # },

    #ORDER ENDPOINTS
    {
        "url": "/api/status/{order_id}",
        "method": "PATCH",
        "path_params": {"order_id": ORDER_ID},
        "auth_required": True
    },

    {
        "url": "/api/orders",
        "method": "GET",
        "query_params": {"timeframe": "today"},
        "auth_required": True
    },
    
    #DISCOUNT ENDPOINTS
    # {
    #     "url": "/api/discount",
    #     "method": "POST",
    #     "body_params": f"{DISCOUNT_DRAFT}",
    #     "auth_required": True
    # },

    {
        "url": "/api/discount/promotions",
        "method": "GET",
        "auth_required": True
    },

    # SHOP ENDPOINTS
    {
        "url": "/api/shop",
        "method": "POST",
        "body_params": SHOP_DRAFT,
        "auth_required": True
 
    },

    # Track user visit to a shop
    {
        "url": "/api/shop/store-traffic",
        "method": "POST",
        "body_params": SHOP_ID,
        "auth_required": True
    },

    # Get all shops
    {
        "url": "/api/shops",
        "method": "GET",
        "auth_required": True
    },
    {
        'url': '/shops/merchant',
        'method': 'GET',
        'auth_required': True
    },
    {
        'url': '/shop/store-traffic/count/{shop_id}',
        'method': 'GET',
        'path_params': {'shop_id': SHOP_ID},
        'auth_required': True
    },

    {
        "url": "/api/shop/{shop_id}",
        "method": "GET",
        "path_params": {"shop_id": SHOP_ID},
        "auth_required": True

    },

    #SALES

    {
        "url": "/api/sales/reports",
        "method": "GET",
        "query_params": {"timeframe": "24hr"},
        "auth_required": True
    },

    #ORDERS
    {
        "url": "/api/Orders/all",
        "method": "GET",
        "auth_required": True
    },

    {
        "url": "/api/orders/average",
        "method": "GET",
        "query_params": {"timeframe": "today"},
        "auth_required": True

    },

    {
        "url": "/api/search/{name}",
        "method": "GET",
        "path_params": {"name": PRODUCT_NAME},
        "auth_required": True
    },

    #REVENUE
    {
        "url": "/api/revenue/{order_id}",
        "method": "PATCH",
        "path_params": {"order_id": ORDER_ID},
        "auth_required": True
    },

    {
        "url": "/api/revenues",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "query_params": {"timeframe": "today"},
        "auth_required": True
    },
]
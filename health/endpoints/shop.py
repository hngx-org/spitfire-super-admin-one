BASE_URL = "https://zuriportfolio-shop-internal-api.onrender.com"
NAME = "SHOP"
PRODUCT_NAME = "Zuri Chat"
PRODUCT_DRAFT = {
    "image": "https://zuri.chat/static/media/logo.36d2d48a.svg",
    "shopId": "",
    "parent_category_id": "Software",
    "sub_category_ids": [1, 2],
    "name": "Zuri Chat",
    "description": "Zuri Chat is a messaging app built for teams",
    "quantity": 100,
    "price": 1000,
    "discount": 900,
    "tax": 100,
    "currency": "USD",
}

PRODUCT_CATEGORY_DRAFT = {
    "name": "Software Enginering",
    "parent_id": ""
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

SHOP_DRAFT = {}

SHOP_ID = ""

ENDPOINTS_CONFIG = [

    # Get all products by name
    {
        "url": "/api/product",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "query_params": {"productname": f"{PRODUCT_NAME}"},
        "auth_required": True
    },

    # Fetch all products
    {
        "url": "/api/products",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "query_params": {"page": 1, "itemsPerPage": 10},
        "auth_required": False
    },
    
    #Fetch all marketplace products
    {
        "url": "/api/products/marketplace",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "query_params": None,
        "auth_required": False
    },

    #Create a product
    {
        "url": "/api/product/add",
        "method": "POST",
        "path_params": None,
        "body_params": f"{PRODUCT_DRAFT}",
        "query_params": None,
        "auth_required": True
    },

    #Create a product Category
    {
        "url": "/api/product/category/add",
        "method": "POST",
        "path_params": None,
        "body_params": f"{PRODUCT_CATEGORY_DRAFT}",
        "query_params": None,
        "auth_required": True
    },

    #Retrieve product categories
    {
        "url": "/api/product/categories",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "query_params": None,
        "auth_required": False
    },

    #Fetch product by id
    {
        "url": "/api/product/{product_id}",
        "method": "GET",
        "path_params": {"product_id": "1"},
        "body_params": None,
        "query_params": None,
        "auth_required": False
    },
    
    #Delete product by id
    {
        "url": "/api/product/{product_id}",
        "method": "DELETE",
        "path_params": {"product_id": "1"},
        "body_params": None,
        "query_params": None,
        "auth_required": True
    },

    # Upload new product image
    {
        "url": "/api/product/{product_id}/image",
        "method": "POST",
        "path_params": {"product_id": "1"},
        "body_params": None,
        "query_params": None,
        "headers": {"Content-Type": "multipart/form-data"},
        "auth_required": True
    },

    #Get product images
    {
        "url": "/api/product/{product_id}/image",
        "method": "GET",
        "path_params": {"product_id": "1"},
        "body_params": None,
        "query_params": None,
        "auth_required": False
    },

    #Update product image
    {
        "url": "/api/product/{product_id}/image/{image_id}",
        "method": "PATCH",
        "path_params": {"product_id": "1", "image_id": "1"},
        "body_params": None,
        "query_params": None,
        "headers": {"Content-Type": "multipart/form-data"},
        "auth_required": True
    },
    
    #Delete product image
    {
        "url": "/api/product/{product_id}/image/{image_id}",
        "method": "DELETE",
        "path_params": {"product_id": "1", "image_id": "1"},
        "body_params": None,
        "query_params": None,
        "auth_required": True
    },

    #ORDER ENDPOINTS
    {
        "url": "/api/status/{order_id}",
        "method": "PATCH",
        "path_params": {"order_id": "1"},
        "body_params": None,
        "query_params": None,
        "auth_required": True
    },

    {
        "url": "/api/orders",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "query_params": {"timeframe": "today"},
        "auth_required": True
    },
    
    #DISCOUNT ENDPOINTS
    {
        "url": "/api/discount",
        "method": "POST",
        "path_params": None,
        "body_params": f"{DISCOUNT_DRAFT}",
        "query_params": None,
        "auth_required": False
    },

    {
        "url": "/api/discount/promotions",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "query_params": None,
        "auth_required": True
    },

    # SHOP ENDPOINTS
    {
        "url": "/api/shop",
        "method": "POST",
        "path_params": None,
        "body_params": f"{SHOP_DRAFT}",
        "query_params": None,
        "auth_required": False
 
    },

    # Track user visit to a shop
    {
        "url": "/api/shop/store-traffic",
        "method": "POST",
        "path_params": None,
        "body_params": f"{SHOP_ID}",
        "query_params": None,
        "auth_required": False
    },

    # Get all shops
    {
        "url": "/api/shops",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "query_params": None,
        "auth_required": True
    },

    {
        "url": "/api/shop/{shop_id}",
        "method": "GET",
        "path_params": {"shop_id": "1"},
        "body_params": None,
        "query_params": None,
        "auth_required": True

    },

    #SALES

    {
        "url": "/api/sales/reports",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "query_params": {"timeframe": "today"},
        "auth_required": True
    },

    #ORDERS
    {
        "url": "/api/Orders/all",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "query_params": None,
        "auth_required": False
    },

    {
        "url": "/api/orders/average",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "query_params": {"timeframe": "today"},
        "auth_required": True

    },

    {
        "url": "/api/search/{name}",
        "method": "GET",
        "path_params": {"name": f"{PRODUCT_NAME}"},
        "body_params": None,
        "query_params": None,
        "auth_required": True
    },

    #REVENUE
    {
        "url": "/api/revenue/{order_id}",
        "method": "PATCH",
        "path_params": {"order_id": "1"},
        "body_params": None,
        "query_params": None,
        "auth_required": False
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
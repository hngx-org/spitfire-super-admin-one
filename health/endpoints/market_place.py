BASE_URL = "https://coral-app-8bk8j.ondigitalocean.app/api"
NAME = "Market Place"

USER_ID = ""
PRODUCT_ID = ""
PRODUCT_INTERACTION = {
    "interaction_type": "view",
    "user": "",
    "product": "",
    "created_at": "",
}

ENDPOINTS_CONFIG = [
    {
        "url": "/add-recently-viewed/{user_id}/{product_id}/",
        "method": "POST",
        "path_params": {
            "user_id": USER_ID,
            "product_id": PRODUCT_ID
        },
        "body_params": {
            "data": PRODUCT_INTERACTION
        },
        "auth_required": True,
    },
    {
        "url": "/category-name/",
        "method": "GET",
        "auth_required": True,
    },
    {
        "url": "/categoryNames/",
        "method": "GET",
        "auth_required": True,
    },
    {
        "url": "/getproduct/{product_id}/{user_id}/",
        "method": "GET",
        "path_params": {
            "product_id": PRODUCT_ID,
            "user_id": USER_ID
        },
        "auth_required": True,
    },
    {
        "url": "/image/{productId}/",
        "method": "GET",
        "path_params": {
            "productId": PRODUCT_ID
        },
    },

    #WORKS
    {
        "url": "/images/",
        "method": "GET",
    },

    {
        "url": "/product-list/",
        "method": "GET",
    },
    {
        "url": "/product-retrieval/",
        "method": "GET",
        "query_params": {

        },
    },
    {
        "url": "/products-filter/",
        "method": "GET",
    },
    {
        "url": "/products-sort/{sorting_option}/",
        "method": "GET",
        "path_params": {
            "sorting_option": "price"
        },
    },
    {
        "url": "/products/limited_offers/",
        "method": "GET",
    },
    {
        "url": "/products/{category}",
        "method": "GET",
        "path_params": {
            "category": "electronics"
        },
    },
    {
        "url": "/products/{category}/{subcategory}/",
        "method": "GET",
        "path_params": {
            "category": "electronics",
            "subcategory": "laptops"
        },
    },
    {
        "url": "/recently-viewed/{user_id}/",
        "method": "GET",
        "path_params": {
            "user_id": USER_ID
        },
    },
    {
        "url": "/recommendations/",
        "method": "GET",
    },
    {
        "url": "/similar_products/{product_id}/",
        "method": "GET",
        "path_params": {
            "product_id": PRODUCT_ID
        },
    },
    {
        "url": "/user-wishlist/{user_id}/",
        "method": "GET",
        "path_params": {
            "user_id": USER_ID
        },
        "auth_required": True,
    },
    {
        "url": "/wishlist/",
        "method": "POST",
        "auth_required": True,
        "body_params": {
            "data": {
                "user_id": USER_ID,
                "product_id": PRODUCT_ID,
            },
        },
        "auth_required": True,
    },
    
    {
        "url": "/wishlist/delete/{user_id}/{product_id}/",
        "method": "DELETE",
        "path_params": {
            "user_id": USER_ID,
            "product_id": PRODUCT_ID,
        },
        "auth_required": True,
    },
]

BASE_URL = "https://customer-purchase.onrender.com"
NAME = "CUSTOMER PURCHASE"
ITEM = "123456789"
PRICE = "123456789"
SERACH_TERM = "123456789"

ENDPOINTS_CONFIG = [

    #TRANSACTIONS
    {
        "url": "api/orders/all-transactions",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True   
    },

    {
        "url": "/api/orders/cancelled-transactions",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "query_params": {
            "status": "cancelled"
        },
        "auth_required": True   
    },

    {
        "url": "/api/orders/failed-transactions",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "query_params": {
            "item": f"{ITEM}",
            "price":f"{PRICE}",
        }
    },

    {
        "url":"api/orders/search-transactions",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "query_params": {
            "search": f"{SERACH_TERM}",
        }
    }
]

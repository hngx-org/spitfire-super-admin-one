BASE_URL = "https://customer-purchase.onrender.com"
NAME = "CUSTOMER PURCHASE"
ITEM = "123456789"
PRICE = "123456789"
SERACH_TERM = "123456789"
ORDERITEMIDS = []

ENDPOINTS_CONFIG = [

    #TRANSACTIONS
    {
        "url": "/api/orders/all-transactions",
        "method": "GET",
        "auth_required": True   
    },

    {
        "url": "/api/orders/cancelled-transactions",
        "method": "GET",
        "query_params": {
            "status": "cancelled"
        },
        "auth_required": True   
    },

    {
        "url": "/api/orders/failed-transactions",
        "method": "GET",
        "query_params": {
            "item": f"{ITEM}",
            "price":f"{PRICE}",
        }
    },
    {
        "url":"/api/orders/search-transactions",
        "method": "GET",
        "query_params": {
            "search": f"{SERACH_TERM}",
        },
        "auth_required": True
    },

    {
        "url": "/api/orders/pending-transactions",
        "method": "GET",
        "auth_required": True

    },

    {
        "url": "/api/orders/completed-transactions",
        "method": "GET",
        "auth_required": True
    },

    {
        "url": "/api/orders/delete-transactions",
        "method": "DELETE",
        "body_params": {
            "orderItemIds":f"{ORDERITEMIDS}"
        },
        "auth_required": True
    }
]

BASE_URL = "https://customer-purchase.onrender.com"
NAME = "CUSTOMER PURCHASE"
SERACH_TERM = "John Doe"
ORDERITEMIDS = [1,2,3]

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
        "url": "/api/orders/filter-transactions",
        "method": "GET",
        "query_params": {
            "status": "2023"
        },
        "auth_required": True
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

    # # RETURNS NOTHING
    # {
    #     "url": "/api/orders/delete-transactions",
    #     "method": "DELETE",
    #     "body_params": {
    #         "orderItemIds":f"{ORDERITEMIDS}"
    #     },
    #     "auth_required": True
    # }
]

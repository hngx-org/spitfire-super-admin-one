BASE_URL = "https://zuri-cart-checkout.onrender.com"
NAME = "Cart Checkout"

ORDER_ID = "123456789"
TRANSACTION_ID = "123456789"
REFERENCE = "123456789"
X_PAYSTACK_SIGNATURE = "123456789"
VERIF_HASH_FLW = "123456789"
PRODUCT_IDS = []
PRODUCT_ID = "123456789"


ENDPOINTS_CONFIG = [

    #ORDERS
    {
        "url": "/api/orders",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "redirect_url": "https://localhost:3001",
            "payment_method": "flutterwave"
        }
        ,
        "auth_required": False
    },

    {
        "url": "/api/orders",
        "method": "PUT",
        "path_params": None,
        "body_params": None,
        "auth_required": False
    },

    {
        "url": "/api/orders/{order_id}",
        "method": "GET",
        "path_params": {
            "order_id": f"{ORDER_ID}"
        },
        "body_params": None,
        "auth_required": False
    },

    #TRANSACTIONS

    {
        "url": "/api/transactions",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": False
    },

    {
        "url": "/api/transactions/{transaction_id}",
        "method": "GET",
        "path_params": {
            "transaction_id": f"{TRANSACTION_ID}"
        },
        "body_params": None,
        "auth_required": False
    },
    
    #PAYMENT METHODS

    {
        "url": "/api/webhooks/flw",
        "method": "GET",
        "path_params": None,
        "body_params": {
            "event": "charge.completed",
            "data": {
                "id": 1234,
                "tx_ref": "Zuri-tx-1697027556476",
                "flw_ref": "b9583b59120d46e3764b",
                "status": "successful",
                "amount": 25.7397,
                "currency": "NGN"
            }
        },
        "headers": {
            "verif-hash": f"{VERIF_HASH_FLW}"
        },
        "auth_required": False
    },

    {
        "url": "api/webhooks/paystack",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "event": "paymentrequest.success",
            "data": {
                "id": f"{TRANSACTION_ID}",
                "domain": "test",
                "reference": f"{REFERENCE}",
                "status": "success",
                "amount": 25.7397,
                "currency": "NGN"
            }
        },
        "headers": {
            "x-paystack-signature": "f{X_PAYSTACK_SIGNATURE}}"
        },
        "auth_required": False
    },

    #CART

    {
        "url": "/api/carts/cart-summary",
        "method": "GET",
        "path_params": None,
        "body_params": None,
        "auth_required": True
    },

    {
        "url": "/api/carts",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "product_ids": f"{PRODUCT_IDS}",
        },
    },

    {
        "url": "/api/carts/{product_id}",
        "method": "DELETE",
        "path_params": {
            "product_id": f"{PRODUCT_ID}"
        },
        "body_params": None,
        "auth_required": True
    }

    

]
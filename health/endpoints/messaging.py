BASE_URL = "https://team-titan.mrprotocoll.me"
PROJECT_NAME = "MESSAGING/ EMAIL"
EMAIL = " "
NAME = " "
BUYER_NAME = " "
SELLER_NAME = " "
BUYER_EMAIL = " "
SELLER_EMAIL = " "
SHOP_NAME = " "
SHOP_EMAIL = " "

ENDPOINTS_CONFIG = [

    #USER
    {
        "url": "/api/messaging/user/account/banned",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recepient": f"{EMAIL}",
            "name": f"{NAME}"
        },
        "auth_required": False
    },

    {
        "url": "/api/messaging/user/account/blacklisted",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recepient": f"{EMAIL}",
            "name": f"{NAME}"
        },
        "auth_required": False
    },

    {
        "url": "/api/messaging/user/account/deleted",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recepient": f"{EMAIL}",
            "name": f"{NAME}"
        },
        "auth_required": False
    },

    {
        "url": "/api/messaging/user/account/suspended",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recepient": f"{EMAIL}",
            "name": f"{NAME}"
        },
        "auth_required": False
    },

    {
        "url": "/api/messaging/user/account/email-verification",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recepient": f"{EMAIL}",
            "name": f"{NAME}"
        },
        "auth_required": False
    },

    {
        "url": "/api/messaging/user/account/password-reset",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recepient": f"{EMAIL}",
            "name": f"{NAME}"
        },
        "auth_required": True
    },

    {
        "url": "/api/messaging/user/account/signup-notification",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recepient": f"{EMAIL}",
            "name": f"{NAME}"
        },
        "auth_required": True
    },

    {
        "url": "/api/messaging/user/account/twoFacttorAuth",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recepient": f"{EMAIL}",
            "name": f"{NAME}"
        },
        "auth_required": False
    },

    {
        "url": "/api/messaging/user/account/welcome-email",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recepient": f"{EMAIL}",
            "name": f"{NAME}"
        },
        "auth_required": True
    },

    #ASSESSEMENT
    {
        "url": "/api/messaging/assessment/buyer-assessment",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recepient": f"{BUYER_EMAIL}",
            "name": f"{BUYER_NAME}",
            "service": "TEST API SERVICE",
            "call_to_action_link": "https://apistatus-test.com"
        },
        "auth_required": False
    },

    {
        "url": "/api/messaging/assessment/seller-assessment",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recepient": f"{SELLER_EMAIL}",
            "buyer_name": f"{BUYER_NAME}",
            "seller_name": f"{SELLER_NAME}",
            "service": "TEST API SERVICE",
            "call_to_action_link": "https://apistatus-test.com"
        },
        "auth_required": False
    },

    {
        "url": "/api/messaging/assessment/badge",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recepient": f"{EMAIL}",
            "name": f"{NAME}",
            "badge_name": "TEST BADGE",
            "call_to_action_link": "https://apistatus-test.com"
        },
        "auth_required": False
    },

    #ORDER
    {
        "url": "/api/messaging/order/buyer-order-confirmation",
        "method": "POST",
        "path_params": None,
        "body_params": {
           {
                "recipient": "{BUYER_EMAIL}",
                "name": f"{BUYER_NAME}",
                "order_details": {
                    "order_id": "#2424352345",
                    "items": [
                        {
                            "image_link": "https://adeleke.tech/hng/headset.png",
                            "item_name": "Brown Nylon Jacket",
                            "item_price": 600
                        }
                    ],
                    "subtotal": 600,
                    "discount_percentage": 10,
                    "shipping": 10,
                    "total": 550
                },
                "billing_information": {
                    "name": f"{BUYER_NAME}",
                    "email": f"{BUYER_EMAIL}",
                }
            }
        },
    },

    {
        "url": "/api/messaging/order/seller-order-confirmation",
        "method": "POST",
        "body_params": {
            "recipient": "{SELLER_EMAIL}",
            "name": "{SELLER_NAME}",
            "order_details": {
                "order_id": "#2424352345",
                "items": [
                    {
                        "image_link": "https://adeleke.tech/hng/headset.png",
                        "item_name": "Brown Nylon Jacket",
                        "item_price": 600
                    }
                ],
                "subtotal": 600,
                "discount_percentage": 10,
                "shipping": 10,
                "total": 550
            },
            "billing_information": {
                "name": "{BUYER_NAME}",
                "email": "{BUYER_EMAIL}"
            }
        },
        "auth_required": False
    },


    {
        "url": "/api/messaging/order/buyer-purchase-confirmation",
        "method": "POST",
        "body_params": {
            "recipient": "{BUYER_EMAIL}",
            "name": "{BUYER_NAME}",
            "order_details": {
                "order_id": "#655922",
                "order_date": "September 16, 2023",
                "total_amount": 20000,
                "items": [
                    {
                        "image_link": "https://img.ur/hudy67.jpg",
                        "course_title": "Introduction to UI/UX",
                        "instructor": "Daviowhite",
                        "access_link": "https://example.com/course-title",
                        "amount": 20000
                    }
                ]
            },
            "billing_information": {
                "name": "{BUYER_NAME}",
                "email": "{BUYER_EMAIL}",
                "payment_method": "Paystack"
            },
            "auth_required": True
        }
    },

    {
        "url": "/api/messaging/order/buyer-purchase-confirmation",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recipient": "{SELLER_EMAIL}",
            "name": "{SELLER_NAME}",
            "order_details": {
                "order_id": "#655922",
                "order_date": "September 16, 2023",
                "total_amount": 20000,
                "items": [
                    {
                        "image_link": "https://img.ur/hudy67.jpg",
                        "course_title": "Introduction to UI/UX",
                        "instructor": "Daviowhite",
                        "access_link": "https://example.com/course-title",
                        "amount": 20000
                    }
                ]
            },
            "buyer_information": {
                "email": "{BUYER_EMAIL}",
                "name": "{BUYER_NAME}"
            },
            "earnings_summary": {
                "total_earnings": 20000,
                "net_earnings": 18000
            },
            "payment_date": "September 17, 2023",
            "support_contact": "support@example.com"
        },
        "auth_required": True
    },

    {
        "url": "api/messaging/order/rating",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recipient": f"{BUYER_EMAIL}",
            "name":     f"{SELLER_NAME}",
            "call_to_action_link": "https://example.com/prduct/1234",
            "order_details": {
                "items": [
                    {
                        "image_link": "https://w7.pngwing.com/pngs/895/199/png-transparent-spider-man-heroes-download-with-transparent-background-free-thumbnail.png",
                        "item_name": "Brown nylon jacket"
                    }
                ]
            }
        },
        "auth_required": False
    },

    # PRODUCT
    {
        "url": "/api/messaging/product/deleted",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recipient": f"{SHOP_EMAIL}",
            "name": f"{SHOP_NAME}",  # Added f before the string placeholder
            "product_name": "How to get rich by sleeping",
            "violation": "You failed to comply with the rules binding on vendors",
            "store_link": "https://zuriportfolio.com/login",
            "image_url": "https://zuriportfolio-frontend-pw1h.vercel.app/assets/images/emails-temp/assessment/green-logo.png",
            "product_info": "This course has sold 121 copies so far"
        },
        "auth_required": True
    },

    {
        "url": "/api/messaging/product/suspended",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recipient": f"{SHOP_EMAIL}",
            "name": f"{SHOP_NAME}",  
            "product_name": "How to get rich by sleeping",
            "violation": "You failed to comply with the rules binding on vendors",
            "store_link": "https://zuriportfolio.com/login",
            "image_url": "https://zuriportfolio-frontend-pw1h.vercel.app/assets/images/emails-temp/assessment/green-logo.png",
            "product_info": "This course has sold 121 copies so far"
        },
        "auth_required": True
    },

    {
        "url": "/api/messaging/product/unsuspended",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recipient": f"{SHOP_EMAIL}",
            "name": f"{SHOP_NAME}",
            "product_name": "Product1",
            "sales_count": "23",
            "product_image_url": "http://example.com/product-image.jpg",
            "store_link": "http://example.com/store",
            "sanction_reason": "Violation of terms and conditions"
        },
        "auth_required": False
    },
    {
        "url": "/api/messaging/store/approved",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recipient": "emekaenyinnia123@gmail.com",
            "name": "Goodnews",
            "call_to_action_link": "https://www.youtube.com",
            "store_name": "market"
    },
    "auth_required": False
    },

    {
    "url": "/api/messaging/store/deleted",
    "method": "POST",
    "path_params": None,
    "body_params": {
        "recipient": "example@email.com",
        "name": "John Doe",
        "store_name": "Store Name"
    },
    "auth_required": False
    },

    {
        "url": "/api/messaging/store/review",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "name": "Test User",
            "recipient": "ruthiejay022@gmail.com",
            "store_name": "Product store",
            "store_link": "https://example.com"
        },
        "auth_required": True
    },

    {
        "url": "/api/messaging/store/suspended",
        "method": "POST",
        "path_params": None,
        "body_params": {
            "recipient": "user@example.com",
            "name": "Dare",
            "store_name": "Road to marketing",
            "reasons": [
                {
                    "reason": "Product misrepresentation"
                }
            ]
        },
        "auth_required": False
    },

    {
            "url": "/api/messaging/store/suspension-lifted",
            "method": "POST",
            "path_params": None,
            "body_params": {
                "recipient": "user@example.com",
                "name": "Dare",
                "store_name": "Road to marketing"
        },
        "auth_required": False
    }


]
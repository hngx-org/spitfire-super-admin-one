from health.helpers import update
from health import USER_ID

BASE_URL = "https://team-titan.mrprotocoll.me"
PROJECT_NAME = "MESSAGING/ EMAIL"

EMAIL = "zurihealthcheck@gmail.com"
NAME = "Farida"
BUYER_NAME = "Farida"
SELLER_NAME = "Kim"
BUYER_EMAIL = "zurihealthcheck@gmail.com"
SELLER_EMAIL = "zurihealthcheck@gmail.com"
SHOP_NAME = "Fari Ventures"
SHOP_EMAIL = "zurihealthcheck@gmail.com"

USER_PARAMS = {
    "recipient": f"{EMAIL}",
    "name": f"{NAME}",
}

SHOP_DETAILS = {

}

ENDPOINTS_CONFIG = [

    #USER
    {
        "url": "/api/messaging/user/account-banned",
        "method": "POST",
        "body_params": USER_PARAMS,

    },

    {
        "url": "/api/messaging/user/account-blacklisted",
        "method": "POST",
        "body_params": USER_PARAMS
    },

    {
        "url": "/api/messaging/user/account-deleted",
        "method": "POST",
        "body_params": update(
            USER_PARAMS,
            {'account_id': USER_ID}
        )
    },

    {
        "url": "/api/messaging/user/account-suspended",
        "method": "POST",
        "body_params": update(
            USER_PARAMS,
            {'violation': 'You failed to comply with vendor rules'}
        )
    },

    {
        "url": "/api/messaging/user/email-verification",
        "method": "POST",
        "body_params": update(
            USER_PARAMS,
            {'verification_link': 'https://staging.zuri.team/testing'}
        )
    },
    {
        "url": "/api/messaging/user/password-reset",
        "method": "POST",
        "body_params": update(
            USER_PARAMS,
            {'reset_link': 'https://staging.zuri.team/testing'}
        )
    },
    {
        'url': '/api/messaging/user/complaint-confirmation',
        'method': 'POST',
        'body_params': update(
            USER_PARAMS,
            {'tracking_number': '12345'}
        ),
        'auth_required': True
    },
    {
        "url": "/api/messaging/user/signup-notification",
        "method": "POST",
        "body_params": USER_PARAMS,
        "auth_required": True
    },

    {
        "url": "/api/messaging/user/twoFactorAuth",
        "method": "POST",
        "body_params": update(
            USER_PARAMS,
            {'code': '12345'}
        ),
    },
    {
        "url": "/api/messaging/user/welcome-email",
        "method": "POST",
        "body_params": update(
            USER_PARAMS,
            {'call_to_action': 'https://staging.zuri.team/testing'}
        ),
        "auth_required": True
    },

    #ASSESSEMENT
    {
        "url": "/api/messaging/assessment/buyer-assessment",
        "method": "POST",
        "body_params": {
            "recepient": f"{BUYER_EMAIL}",
            "name": f"{BUYER_NAME}",
            "service": "TEST API SERVICE",
            "call_to_action_link": "https://staging.zuri.team/testing"
        },

    },

    {
        "url": "/api/messaging/assessment/seller-assessment",
        "method": "POST",
        "body_params": {
            "recepient": f"{SELLER_EMAIL}",
            "buyer_name": f"{BUYER_NAME}",
            "seller_name": f"{SELLER_NAME}",
            "service": "TEST API SERVICE",
            "call_to_action_link": "https://apistatus-test.com"
        },
    },

    {
        "url": "/api/messaging/assessment/badge",
        "method": "POST",
        "body_params": {
            "recepient": f"{EMAIL}",
            "name": f"{NAME}",
            "badge_name": "TEST BADGE",
            "call_to_action_link": "https://staging.zuri.team/testing"
        },
    },

    #ORDER
    {
        "url": "/api/messaging/order/buyer-order-confirmation",
        "method": "POST",
        "body_params": {
                "recipient": f"{BUYER_EMAIL}",
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

    {
        "url": "/api/messaging/order/seller-order-confirmation",
        "method": "POST",
        "body_params": {
            "recipient": f"{SELLER_EMAIL}",
            "name": f"{SELLER_NAME}",
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
                "email": f"{BUYER_EMAIL}"
            }
        },
        "auth_required": False
    },


    {
        "url": "/api/messaging/order/buyer-purchase-confirmation",
        "method": "POST",
        "body_params": {
            "recipient": f"{BUYER_EMAIL}",
            "name": f"{BUYER_NAME}",
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
                "name": f"{BUYER_NAME}",
                "email": f"{BUYER_EMAIL}",
                "payment_method": "Paystack"
            },
            "auth_required": True
        }
    },

    {
        "url": "/api/messaging/order/buyer-purchase-confirmation",
        "method": "POST",
        "body_params": {
            "recipient": f"{SELLER_EMAIL}",
            "name": f"{SELLER_NAME}",
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
                "email": f"{BUYER_EMAIL}",
                "name": f"{BUYER_NAME}"
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
    },

    # PRODUCT
    {
        "url": "/api/messaging/product/deleted",
        "method": "POST",
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
        "url": "/api/messaging/product/suspended",
        "method": "POST",
        "body_params": {
            "recipient": f"{SHOP_EMAIL}",
            "name": f"{SHOP_NAME}",  
            "product_name": "How to get rich by sleeping",
            "violation": "You failed to comply with the rules binding on vendors",
            "image_url": "https://zuriportfolio-frontend-pw1h.vercel.app/assets/images/emails-temp/assessment/green-logo.png",
            "product_info": "This course has sold 121 copies so far"
        },
    },

    {
        "url": "/api/messaging/product/unsuspended",
        "method": "POST",
        "body_params": {
            "recipient": f"{SHOP_EMAIL}",
            "name": f"{SHOP_NAME}",
            "product_name": "Product1",
            "sales_count": "23",
            "product_image_url": "http://example.com/product-image.jpg",
            "store_link": "http://example.com/store",
            "sanction_reason": "Violation of terms and conditions"
        },
    },
    {
        "url": "/api/messaging/store/approved",
        "method": "POST",
        "body_params": update(
            USER_PARAMS,
            {
                "call_to_action_link": "https://staging.zuri.team/testing",
                "store_name": "market"
            }
        ),
    },

    {
        "url": "/api/messaging/store/deleted",
        "method": "POST",
        "body_params": update(
            USER_PARAMS,
            {'store_name': 'Test Store'}
        ),
    },

    {
        "url": "/api/messaging/store/review",
        "method": "POST",
        "body_params": update(
            USER_PARAMS,
            {
                'store_name': 'Test Store',
                'store_link': 'https://staging.zuri.team/testing'
            }
        ),
        "auth_required": True
    },

    {
        "url": "/api/messaging/store/suspended",
        "method": "POST",
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
    },

    {
            "url": "/api/messaging/store/suspension-lifted",
            "method": "POST",
            "body_params": {
                "recipient": "user@example.com",
                "name": "Dare",
                "store_name": "Road to marketing"
        },
    },
    {
        'url': '/api/messaging/store/warning',
        'method': 'POST',
        'body_params': update(
            USER_PARAMS,
            {'store_name': 'Test Store'}
        ),
        'auth_required': True
    }


]
BASE_URL = "https://team-liquid-repo.onrender.com"
NAME = "REVIEWS"
PRODUCT_ID = "023a01f9-6d84-4010-908c-ba6e20c21287"
REVIEW_ID = 2
RATING_NO = 3
sortingParameter = ""


async def extract_review_id(response: dict):
    return 'product_review', response.get("data").get("reviewId")

ENDPOINTS_CONFIG = [
    #rating-controller
    {
        "url": "/api/review/products/rating/{productId}/rating",
        "method": "POST",
        "path_params": {"productId": f"{PRODUCT_ID}"},
        "query_params": {"ratingNo": f"{RATING_NO}",},
    },

    {
        "url": "/api/review/products/{productId}/rating",
        "method": "GET",
        "path_params": {"productId": f"{PRODUCT_ID}"},
    },
    #review-controller
    {
        "url": "/api/review/shop/reviews/{reviewId}",
        "method": "POST",
        "path_params": {"reviewId": f"{REVIEW_ID}"},
        "body_params": {
            'name': 'A name',
            'feedback': 'A feedback',
        },
    },

    # {
    #     "url": "/api/review/products/{productId}/reviews",
    #     "method": "POST",
    #     "path_params": {"productId": f"{PRODUCT_ID}"},
    #     "body_params": {
    #         "customerName": "Zuri tester",
    #         "description": "Just a random test",
    #         "rateNo": 4,
    #     },
    #     "extractor": extract_review_id,
    # },
    # {
    #     "url": "/api/review/products/{}",
    #     "method": "DELETE",
    # },

    {
        "url": "/api/review/products/review/{reviewId}",
        "method": "POST",
        "path_params": {"reviewId": f"{REVIEW_ID}"},
    },

    {
        "url": "/api/review/shop/{productId}/reviews",
        "method": "GET",
        "path_params": {"productId": f"{PRODUCT_ID}"},
    },

    {
        "url": "/api/review/shop/products/{productId}/reviews/rating",
        "path_params": {"productId": f"{PRODUCT_ID}"},
        "method": "GET",
        "query_params": {"rating": RATING_NO},
    },

    {
        "url": "/api/review/products/{productId}/reviews/sort",
        "path_params": {"productId": f"{PRODUCT_ID}"},
        "method": "GET",
        "query_params": {"sortingParameter": "newest"},
    },

    {
        "url": "/api/review/products/reviews/{reviewId}",
        "path_params": {"reviewId": f"{REVIEW_ID}"},
        "method": "GET",
    },

    {
        "url": "/api/review/marketplace/products/{productId}/reviews",
        "path_params": {"productId": f"{PRODUCT_ID}"},
        "method": "GET",
        "query_params": {"pageNumber": 1, "pageSize": 10},
    },

    {
        "url": "/api/review/marketplace/products/{productId}/reviews/rating",
        "path_params": {"productId": f"{PRODUCT_ID}"},
        "method": "GET",
        "query_params": {"rating": RATING_NO},
    },



]
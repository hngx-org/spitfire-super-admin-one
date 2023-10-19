BASE_URL = "https://team-liquid-repo.onrender.com"
NAME = "REVIEWS"
PRODUCT_ID = ""
REVIEW_ID = ""
ratingNo = ""
rating = ""
sortingParameter = ""



ENDPOINTS_CONFIG = [
    # rating-controller
    {
        "url": "/api/review/products/rating/{productId}/rating",
        "method": "POST",
        "path_params": {"productId": f"{PRODUCT_ID}"},
        "body_params": None,
        "query_params": {"ratingNo": f"{ratingNo}",},
        "auth_required": False
    },

    {
        "url": "/api/review/products/{productId}/rating",
        "method": "GET",
        "path_params": {"productId": f"{PRODUCT_ID}"},
        "body_params": None,
        "query_params": None,
        "auth_required": False
    },
    # review-controller
    {
        "url": "/api/review/shop/reviews/{reviewId}",
        "method": "POST",
        "path_params": {"reviewId": f"{REVIEW_ID}"},
        "body_params": None,
        "query_params": None,
        "auth_required": False
    },

    {
        "url": "/api/review/products/{productId}/reviews",
        "method": "POST",
        "path_params": {"productId": f"{PRODUCT_ID}"},
        "body_params": None,
        "query_params": None,
        "auth_required": False
    },

    {
        "url": "/api/review/products/review/{reviewId}",
        "method": "POST",
        "path_params": {"reviewId": f"{REVIEW_ID}"},
        "body_params": None,
        "query_params": None,
        "auth_required": False
    },

    {
        "url": "/api/review/shop/{productId}/reviews",
        "method": "GET",
        "path_params": {"productId": f"{PRODUCT_ID}"},
        "body_params": None,
        "query_params": {"pageNumber": 1, "pageSize": 10},
        "auth_required": False
    },

    {
        "url": "/api/review/shop/products/{productId}/reviews/rating",
        "path_params": {"productId": f"{PRODUCT_ID}"},
        "method": "GET",
        "body_params": None,
        "query_params": {"rating": f"{rating}", "pageNumber": 1, "pageSize": 10},
        "auth_required": False
    },

    {
        "url": "/api/review/products/{productId}/reviews/sort",
        "path_params": {"productId": f"{PRODUCT_ID}"},
        "method": "GET",
        "body_params": None,
        "query_params": {"sortingParameter": f"{sortingParameter}", "pageNumber": 1, "pageSize": 10},
        "auth_required": False
    },

    {
        "url": "/api/review/products/reviews/{reviewId}",
        "path_params": {"reviewId": f"{REVIEW_ID}"},
        "method": "GET",
        "body_params": None,
        "query_params": None,
        "auth_required": False
    },

    {
        "url": "/api/review/marketplace/products/{productId}/reviews",
        "path_params": {"productId": f"{PRODUCT_ID}"},
        "method": "GET",
        "body_params": None,
        "query_params": {"pageNumber": 1, "pageSize": 10},
        "auth_required": False
    },

    {
        "url": "/api/review/marketplace/products/{productId}/reviews/rating",
        "path_params": {"productId": f"{PRODUCT_ID}"},
        "method": "GET",
        "body_params": None,
        "query_params": {"rating": f"{rating}", "pageNumber": 1, "pageSize": 10},
        "auth_required": False
    },

    {
        "url": "/api/review/products/{reviewId}",
        "path_params": {"reviewId": f"{REVIEW_ID}"},
        "method": "DELETE",
        "body_params": None,
        "query_params": None,
        "auth_required": False
    }


]
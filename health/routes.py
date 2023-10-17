from flask import jsonify

from health import health
from health import health_logger
from health.helpers import check_endpoint, save_logs, clean_up

from health.endpoints.auth import (
    ENDPOINTS_CONFIG as auth,
    BASE_URL as auth_url,
    NAME as auth_name,
)
from health.endpoints.portfolio import (
    ENDPOINTS_CONFIG as portfolio,
    BASE_URL as portfolio_url,
    NAME as portfolio_name,
)
from health.endpoints.badges import (
    ENDPOINTS_CONFIG as badges,
    BASE_URL as badges_url,
    NAME as badges_name,
)
from health.endpoints.superadmin_1 import (
    ENDPOINTS_CONFIG as superadmin_1,
    BASE_URL as superadmin_1_url,
    NAME as superadmin_1_name,
)
from health.endpoints.superadmin_2 import (
    ENDPOINTS_CONFIG as superadmin_2,
    BASE_URL as superadmin_2_url,
    NAME as superadmin_2_name,
)
from health.endpoints.create_assessments import (
    ENDPOINTS_CONFIG as assessments,
    BASE_URL as assessments_url,
    NAME as assessments_name
)
from health.endpoints.take_assessments import (
    ENDPOINTS_CONFIG as take_assessments,
    BASE_URL as take_assessments_url,
    NAME as take_assessment_name
)
from health.endpoints.messaging import (
    ENDPOINTS_CONFIG as messaging_endpoints,
    BASE_URL as messaging_base_url,
    PROJECT_NAME as messaging_name
)
from health.endpoints.market_place import (
    ENDPOINTS_CONFIG as market,
    BASE_URL as market_url,
    NAME as market_name,
)
from health.endpoints.shop import (
    ENDPOINTS_CONFIG as shop,
    BASE_URL as shop_url,
    NAME as shop_name
)
from health.endpoints.cart_checkout import (
    ENDPOINTS_CONFIG as cart,
    BASE_URL as cart_url,
    NAME as cart_name
)
from health.endpoints.customer_purchase import (
    ENDPOINTS_CONFIG as purchase_endpoints,
    BASE_URL as purchase_base_url,
    NAME as purchase_name
)
from health.endpoints.reviews import (
    ENDPOINTS_CONFIG as reviews,
    BASE_URL as reviews_url,
    NAME as reviews_name
)


ENDPOINTS_CONFIGS = [
    # (auth_url, auth, auth_name),
    (superadmin_1_url, superadmin_1, superadmin_1_name),
    # (portfolio_url, portfolio, portfolio_name),
    # (badges_url, badges, badges_name),
    # (shop_url, shop, shop_name),
    #(assessments_url, assessments, assessments_name),
    # (take_assessments_url, take_assessments, take_assessment_name),
    # (messaging_base_url, messaging_endpoints, messaging_name),
    # (market_url, market, market_name),
    # (shop_url, shop, shop_name),
    # (purchase_base_url, purchase_endpoints, purchase_name),
    # (cart_url, cart, cart_name),
    # (reviews_url, reviews, reviews_name),
    # (superadmin_2_url, superadmin_2, superadmin_2_name),
]

TO_CLEAN = []

@health.route("/", methods=["GET"])
def run_checks():
    global TO_CLEAN
    health_results: dict[str, list] = {}

    for base_url, endpoints, name in ENDPOINTS_CONFIGS:
        if health_results.get(name) is None:
            health_results[name] = []

        for config in endpoints:
            endpoint, status, TO_CLEAN = check_endpoint(base_url, config, TO_CLEAN)
            print(endpoint, status)
            print('IDs left to clean:', TO_CLEAN)
            
            health_results[name].append({"endpoint": endpoint, "status": status})

        for table, obj_id in TO_CLEAN:
            clean_up(table, obj_id)

    try:
        save_logs(health_results)
    except Exception as e:
        health_logger.error(f"Error occurred while saving health check logs: {e}")

    return jsonify(health_results), 200
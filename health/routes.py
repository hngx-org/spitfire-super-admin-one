from flask import jsonify

from health import health
from health import health_logger
from health.helpers import check_endpoint, save_logs

from health.endpoints.superadmin_1 import (
    ENDPOINTS_CONFIG as shop_endpoints,
    BASE_URL as shop_base_url,
    NAME as shop_name
)
from health.endpoints.create_assessments import (
    ENDPOINTS_CONFIG as assessments_endpoints,
    BASE_URL as assessments_base_url,
    NAME as assessments_name
)
from health.endpoints.messaging import (
    ENDPOINTS_CONFIG as messaging_endpoints,
    BASE_URL as messaging_base_url,
    PROJECT_NAME as messaging_name
)
from health.endpoints.customer_purchase import (
    ENDPOINTS_CONFIG as purchase_endpoints,
    BASE_URL as purchase_base_url,
    NAME as purchase_name
)


ENDPOINTS_CONFIGS = [
    (shop_base_url, shop_endpoints, shop_name),
    (assessments_base_url, assessments_endpoints, assessments_name),
    (messaging_base_url, messaging_endpoints, messaging_name),
    (purchase_base_url, purchase_endpoints, purchase_name)
]


@health.route("/", methods=["GET"])
def run_checks():
    health_results: dict[str, list] = {}

    for base_url, endpoints, name in ENDPOINTS_CONFIGS:
        if health_results.get(name) is None:
            health_results[name] = []

        for config in endpoints:
            endpoint, status = check_endpoint(base_url, config)
            print(endpoint, status)
            
            health_results[name].append({"endpoint": endpoint, "status": status})

    try:
        save_logs(health_results)
    except Exception as e:
        health_logger.error(f"Error occurred while saving health check logs: {e}")

    return jsonify(health_results), 200
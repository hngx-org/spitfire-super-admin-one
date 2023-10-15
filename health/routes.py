from flask import Blueprint, jsonify

from health.helpers import check_endpoint, save_logs
from health.endpoints.superadmin_1 import (
    ENDPOINTS_CONFIG as shop_endpoints,
    BASE_URL as shop_base_url,
    NAME as shop_name
)
from health.endpoints.assessments import (
    ENDPOINTS_CONFIG as assessments_endpoints,
    BASE_URL as assessments_base_url,
    NAME as assessments_name
)

from . import health

endpoints_configs = [
    (shop_base_url, shop_endpoints, shop_name),
    (assessments_base_url, assessments_endpoints, assessments_name)
]

@health.route("/", methods=["GET"])
def check_endpoints():
    health_results: dict[str, list] = {}

    for base_url, endpoints, name in endpoints_configs:
        if health_results.get(name) is None:
            health_results[name] = []

        for config in endpoints:
            endpoint, status = check_endpoint(base_url, config)
            print(endpoint, status)
            
            health_results[name].append({"endpoint": endpoint, "status": status})

    save_logs(health_results)

    return jsonify(health_results), 200
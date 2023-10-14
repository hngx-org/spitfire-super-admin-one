from flask import Blueprint, jsonify
from health.helpers import check_endpoint
from health.endpoint_config import ENDPOINTS_CONFIG

health = Blueprint("health", __name__, url_prefix="/api/admin/health")
endpoints_config = ENDPOINTS_CONFIG

@health.route("/endpoint", methods=["GET"])
def check_endpoints(endpoints_config=endpoints_config):
    health_results = []

    for endpoint_name, config in endpoints_config.items():
        status = check_endpoint(config)
        health_results.append({"endpoint": endpoint_name, "status": status})

    return jsonify(health_results), 200
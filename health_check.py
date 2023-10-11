import requests
from functools import wraps
from flask import jsonify, Blueprint
from functools import wraps


# List to store working and non-working endpoints
WORKING_ENDPOINTS = []
NON_WORKING_ENDPOINTS = []

def check_services_health(endpoint_function):
    @wraps(endpoint_function)
    def wrapper(*args, **kwargs):
        try:
            # Execute the endpoint function to check its health
            response = endpoint_function(*args, **kwargs)
            print("I happened")
            # Check the response status to determine the health status
            if response.status_code == 200:
                if endpoint_function.__name__ in NON_WORKING_ENDPOINTS:
                    NON_WORKING_ENDPOINTS.remove(endpoint_function.__name__)
                WORKING_ENDPOINTS.append(endpoint_function.__name__)
                return jsonify({"status": "ok", "message": f"{endpoint_function.__name__} is operational."}), 200
            else:
                if endpoint_function.__name__ not in NON_WORKING_ENDPOINTS:
                    NON_WORKING_ENDPOINTS.append(endpoint_function.__name__)
                return jsonify({"status": "error", "message": f"{endpoint_function.__name__} returned an error status code."}), 500

        except Exception as e:
            if endpoint_function.__name__ not in NON_WORKING_ENDPOINTS:
                NON_WORKING_ENDPOINTS.append(endpoint_function.__name__)
            return jsonify({"status": "error", "message": f"{endpoint_function.__name__} encountered an exception: {str(e)}"}), 500
    return wrapper


health_check_blueprint = Blueprint('health_check', __name__)

@health_check_blueprint.route('/api/health', methods=['GET'])
def health_check():
    if not NON_WORKING_ENDPOINTS:
        return jsonify({"status": "ok", "message": "All endpoints are operational.", "working_endpoints": WORKING_ENDPOINTS}), 200
    else:
        return jsonify({"status": "error", "message": "Some endpoints are not operational.", "working_endpoints": WORKING_ENDPOINTS, "non_working_endpoints": NON_WORKING_ENDPOINTS}), 500




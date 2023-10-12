import logging, os
from flask import jsonify, Blueprint, current_app as app
import datetime
from dotenv import load_dotenv

load_dotenv(".env")

logging.basicConfig(filename='health_check.log', level=logging.ERROR)

health_check_blueprint = Blueprint("health_check", __name__, url_prefix="/api/health")

shop_id = os.environ.get("SHOP_ID")
product_id = os.environ.get("PRODUCT_ID")

health_check_logs = []

ENDPOINTS_TO_CHECK = [
    ("shop_endpoint", "GET", "/api/shop/endpoint"),
    ("get_all_shops", "GET", "/api/shop/all"),
    ("get_shop", "GET", f"/api/shop/{shop_id}"),
    ("get_shop_products", "GET", f"/api/shop/all/products"),
    ("get_shop_products - (by id)", "GET", f"/api/shop/{shop_id}/products"),
    ("ban_vendor", "PUT", f"/api/shop/ban_vendor/{shop_id}"),  
    ("get_banned_vendors", "GET", "/api/shop/banned_vendors"),
    ("unban_vendor", "PUT", f"/api/shop/unban_vendor/{shop_id}"),  
    ("delete_shop", "PATCH",f"/api/shop/delete_shop/{shop_id}"),
    ("get_temporarily_deleted_vendors", "GET", f"/api/shop/temporarily_deleted_vendors"),
    ("restore_shop", "PATCH",f"/api/shop/restore_shop/{shop_id}"),
    ("get_all_shop_logs", "GET","/api/logs/shops"),
    ("download_shop_logs", "GET", "/api/logs/shops/download"),
    ("shop_actions", "GET", "/api/logs/shop/actions"),
    ("get_products", "GET", "/api/product/all"),
    ("get_product", "GET", f"/api/product/{product_id}"),
    ("temporary_delete", "PATCH", f"/api/product/delete_product/{product_id}"),
    ("to_restore_product", "PATCH", f"/api/product/restore_product/{product_id}"),
    ("permanent_delete", "DELETE", f"/api/product/delete_product/{product_id}"),
    ("sanctioned_products", "GET", "/api/product/sanctioned"),
    ("log", "GET", "/api/logs/product/download"),
    ("test_notification", "POST", "/api/notification"),
    
]

@health_check_blueprint.route("/", methods=["GET"])
def health():
    health_results = []

    for endpoint_name, http_method, endpoint_url in ENDPOINTS_TO_CHECK:
        status = check_endpoint(endpoint_url, http_method)
        health_results.append({"endpoint": endpoint_name, "status": status})
        
    # Log health check results along with timestamp
    log_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {"timestamp": log_timestamp, "results": health_results}
    health_check_logs.append(log_entry)

    return jsonify(health_results)

@health_check_blueprint.route("/last_check", methods=["GET"])
def last_check():
    # Retrieve the last health check log entry
    if health_check_logs:
        last_check_entry = health_check_logs[-1]
        return jsonify(last_check_entry)
    else:
        return jsonify({"message": "No health check logs available"}), 404

def check_endpoint(endpoint_url, http_method):
    base_url = "http://127.0.0.1:5000"
    full_url = f"{base_url}{endpoint_url}"
    try:
        if http_method == "GET":
            response = app.test_client().get(full_url)
        elif http_method == "PUT":
            response = app.test_client().put(full_url)
        elif http_method == "POST":
            response = app.test_client().post(full_url)
        elif http_method == "DELETE":
            response = app.test_client().delete(full_url)
        elif http_method == "PATCH":
            response = app.test_client().patch(full_url)
        else:
            return "invalid method"

        response_data = response.data.decode('utf-8')  # Convert bytes to string
        print(f"Response from {full_url}: {response_data}")  # Print the response content

        success_code = [200, 201, 204, 404, 403, 401]
        if response.status_code in success_code:
            return "active"
        else:
            logging.error(f"Error occurred while checking {full_url}. Status Code: {response.status_code}")
            return "inactive"
    except Exception as e:
        logging.error(f"Error occurred while checking {full_url}: {e}")
        return "inactive"
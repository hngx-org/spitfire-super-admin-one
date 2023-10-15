import json, time
from datetime import datetime, timedelta
import os

import requests

from health.get_access_token import get_access_token
from health import health_logger


LOGS_DIR = os.getenv("LOGS_DIR", "/tmp/zuri-logs/health/")


def get_full_url(base_url, path):  
    return f"{base_url}{path}"


access_token_info = {
    "token": None,
    "expiration_time": 0
}

def check_endpoint(base_url: str, config: "list[dict]"):
    global access_token_info
    url = get_full_url(base_url, config["url"])
    path_params = config.get("path_params", None)
    body_params = config.get("body_params", None)
    auth_required = config.get("auth_required", False)
    methods_dict ={
        "GET": requests.get,
        "POST": requests.post,
        "PUT": requests.put,
        "PATCH": requests.patch,
        "DELETE": requests.delete
    }
    method = methods_dict.get(config["method"])
    if not method:
        return "invalid method"

    # Replace path parameters in the URL
    if path_params:
        url = url.format(**path_params)

    headers = {}
    if auth_required:
        current_time = time.time()

        # If the access token is not cached or has expired, generate a new one
        if access_token_info["token"] is None or access_token_info["expiration_time"] < current_time:
            new_access_token = get_access_token()

            # Set new access token and its expiration time
            access_token_info["token"] = new_access_token
            access_token_info["expiration_time"] = current_time + 900  # 15 minutes expiration time

        # Use cached access token for the request
        headers["Authorization"] = f"Bearer {access_token_info['token']}"

    endpoint = f"{config['method']} {url}"

    try:
        if method in ["POST", "PUT"] and body_params:
            resp = method(url, headers=headers, json=json.dumps(body_params))
        else:
            resp = method(url, headers=headers)
        status_code = resp.status_code

        print(f"Status code: {status_code}")    

        # Check for expected status codes indicating success
        if resp.status_code in [200, 201, 204]:
            return endpoint, "active", 
        else:
            health_logger.error(f"Error occurred while checking {url}. Unexpected response code: {status_code}")
            return endpoint, "inactive"
    except Exception as err:
        health_logger.error(f"Error occurred while checking {url}: {err}")
        return endpoint, "inactive"
    

def save_logs(logs: "list[dict[str, list]]"):
    """
    Save health check logs to a file in the logs directory

    :param log: logs to save
    """
    # Create logs directory if it doesn't exist
    os.makedirs(LOGS_DIR, exist_ok=True)

    filename = f"{datetime.now().isoformat()}.log"

    with open(os.path.join(LOGS_DIR, filename), "w") as f:
        json.dump(logs, f, indent=4)

    # clear logs older than 7 days
    seven_days = timedelta(days=7)

    for log_file in os.scandir(LOGS_DIR):
        if log_file.is_file():
            datetime_str = f"{log_file.name.split('.')[0]}."\
                            f"{log_file.name.split('.')[1]}"

            save_time = datetime.fromisoformat(datetime_str)
            if datetime.now() - save_time > seven_days:
                os.remove(log_file.path)

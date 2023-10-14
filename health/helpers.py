import subprocess, logging, json, time
from health.get_access_token import get_access_token

access_token = get_access_token()


def get_full_url(relative_url):
    base_url = "https://spitfire-superadmin-1.onrender.com"  
    return base_url + relative_url


access_token_info = {
    "token": None,
    "expiration_time": 0
}

def check_endpoint(config):
    global access_token_info
    url = get_full_url(config["url"])
    method = config["method"]
    path_params = config.get("path_params", {})
    body_params = config.get("body_params", {})
    auth_required = config.get("auth_required", False)

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

    curl_command = ["curl", "-X", method, url, "--write-out", "%{http_code}", "--silent", "--output", "/dev/null"]
    curl_command.extend(["-H", "Content-Type: application/json"])

    if headers:
        header_strings = [f"{k}: {v}" for k, v in headers.items()]
        curl_command.extend(["-H", *header_strings])

    if method in ["POST", "PUT"] and body_params:
        data_string = json.dumps(body_params)  # Convert body_params dictionary to JSON string
        curl_command.extend(["-d", data_string])
    
    # print("Final curl command:")
    # print(" ".join(curl_command))  

    try:
        response_code = int(subprocess.check_output(curl_command))
        # Check for expected status codes indicating success
        if response_code in [200, 201, 204]:
            return "active"
        else:
            logging.error(f"Error occurred while checking {url}. Unexpected response code: {response_code}")
            return "inactive"
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while checking {url}: {e.output}")
        return "inactive"
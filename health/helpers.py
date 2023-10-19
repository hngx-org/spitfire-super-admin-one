import json, time
from datetime import datetime, timedelta
import os
from typing import Callable

import psycopg2

import aiohttp
import time

from health.get_access_token import get_access_token
from health import health_logger


LOGS_DIR = os.getenv(
    "LOGS_DIR",
    os.path.join(os.path.abspath("."), "logs/health")
)
DB_URL = os.getenv('SQLALCHEMY_DATABASE_URI')


access_token_info = {
    "token": None,
    "expiration_time": 0
}


def get_full_url(base_url: str, path: str) -> str:  
    return f"{base_url}{path}"


def update(obj: dict, update_dict: dict) -> dict:
    """
    Update a dictionary with attributes
    from another dictionary

    :param obj: dictionary to update
    :param update_dict: dictionary with attributes to update with

    :return: updated dictionary
    """
    obj.update(update_dict)
    return obj


async def check_endpoint(
    base_url: str,
    config: "list[dict]",
    to_clean: "list[tuple]",
) -> "tuple[str, str]":
    """
    Check the health of an endpoint asynchronously

    :param base_url: base url of the endpoint
    :param config: configuration for the endpoint
    :param to_clean: list of tuples to be cleaned up
    :param access_token_info: information about access token
    :param health_logger: logger for health checks

    :return: endpoint and its status
    """
    global access_token_info
    url = get_full_url(base_url, config["url"])
    query_params = config.get("query_params", None)
    path_params = config.get("path_params", None)
    body_params = config.get("body_params", None)
    headers = config.get("headers", {})
    auth_required = config.get("auth_required", False)
    # methods_dict ={
    #     "GET": requests.get,
    #     "POST": requests.post,
    #     "PUT": requests.put,
    #     "PATCH": requests.patch,
    #     "DELETE": requests.delete
    # }
    methods_dict ={
        "GET": aiohttp.ClientSession.get,
        "POST": aiohttp.ClientSession.post,
        "PUT": aiohttp.ClientSession.put,
        "PATCH": aiohttp.ClientSession.patch,
        "DELETE": aiohttp.ClientSession.delete
    }
    method_name = config["method"]
    method = methods_dict.get(method_name)
    extractor: Callable = config.get("extractor")
    if not method:
        return "invalid method"

    # Replace path parameters in the URL
    if path_params:
        url = url.format(**path_params)

    if auth_required:
        current_time = time.time()

        # If the access token is not cached or has expired, generate a new one
        if access_token_info["token"] is None or access_token_info["expiration_time"] < current_time:
            new_access_token = get_access_token()

            # Set new access token and its expiration time
            access_token_info["token"] = new_access_token
            access_token_info["expiration_time"] = current_time + 900  # 15 minutes expiration time

        if "token" in headers:
            headers["token"] = access_token_info['token']
        else:
            # Use cached access token for the request
            headers["Authorization"] = f"Bearer {access_token_info['token']}"

    endpoint = f"{config['method']} {url}"
    response_json = None
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            if method_name in ["POST", "PUT"] and body_params:
                async with session.request(method_name,url, headers=headers, params=query_params, json=body_params) as resp:
                    status_code = resp.status
                    #print(status_code)
                    response_json = await resp.json() 
                    #print(response_json)

            else:
                if method_name == "DELETE":
                    endpoint = endpoint.format(to_clean[-1][1])
                    url = url.format(to_clean[-1][1])
                async with session.request(method_name, url, headers=headers, params=query_params) as resp:
                    status_code = resp.status
                    #print(status_code)
                    response_json = await resp.json()
                    #print(response_json)
            

        # Check for expected status codes indicating success
        if status_code not in  [500, 502, 503, 504, 401, 403]:
            if extractor:
                id_to_clean = extractor(resp.json())
                print('table and id extracted', id_to_clean)
                to_clean.append(id_to_clean)
            if method_name == "DELETE":
                to_clean.pop()
            return endpoint, "active", to_clean
        else:
            health_logger.error(f"Error occurred while checking {url}."
                                f"Unexpected response code: {status_code}")
            return endpoint, "inactive", to_clean
    except Exception as err:
        health_logger.error(f"Error occurred while checking {url}: {err}")
        return endpoint, "inactive", to_clean

    

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


def clean_up(table: str, obj_id: str):
    """
    Delete an object from the database as
    a clean up

    :param table: table to delete from
    :param obj_id: id of the object to delete

    :return: None
    """
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table} WHERE id = '{obj_id}'")
    conn.commit()

    cur.close()
    conn.close()

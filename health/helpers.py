import json, time
from datetime import datetime, timedelta
import os
from typing import Callable

import httpx
import psycopg2

from health.get_access_token import get_access_token
from health import health_logger


get_access_token()

LOGS_DIR = os.getenv(
    "LOGS_DIR",
    os.path.join(os.path.abspath("."), "logs/health")
)
DB_URL = os.getenv('SQLALCHEMY_DATABASE_URI')
TO_CLEAN = []

access_token_info = {
    "token": os.getenv("ACCESS_TOKEN"),
    "expiration_time": time.time() + 900
}


async def get_full_url(base_url: str, path: str) -> str:  
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
    session: httpx.AsyncClient,
    base_url: str,
    config: "list[dict]",
    # to_clean: "list[tuple]"
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
    url = await get_full_url(base_url, config["url"])
    query_params = config.get("query_params", None)
    path_params = config.get("path_params", None)
    body_params = config.get("body_params", None)
    is_form = config.get("is_form_data", False)
    headers = config.get("headers", {})
    auth_required = config.get("auth_required", False)
    extractor: Callable = config.get("extractor")
    methods_dict ={
        "GET": session.get,
        "POST": session.post,
        "PUT": session.put,
        "PATCH": session.patch,
        "DELETE": session.delete
    }
    method_name = config["method"]
    method = methods_dict.get(method_name)
    if not method:
        return None, "invalid method", TO_CLEAN

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
    resp = None
    try:
        if method_name in ["POST", "PUT"] and body_params:
            params = {
                "params": query_params,
                "headers": headers,
                "data": body_params
            } if is_form else {
                "params": query_params,
                "headers": headers,
                "json": body_params
            }
            resp = await method(url, **params)
        else:
            if method_name == "DELETE":
                obj_id = TO_CLEAN[-1][1]
                if not obj_id:
                    return endpoint, "inactive", TO_CLEAN

                endpoint = endpoint.format(obj_id)
                url = url.format(obj_id)
                ## print(url)
            resp = await method(url, headers=headers, params=query_params)

        status_code = resp.status_code
        # print('status code: ', status_code)
        # print(resp.json())

        # Check for expected status codes indicating success
        if status_code in  [200, 201, 202, 204, 400, 404, 409]:
            if extractor:
                #print('response from POST', resp.json())
                id_to_clean = await extractor(resp.json())
                # # print('table and id extracted', id_to_clean)
                TO_CLEAN.append(id_to_clean)
            if method_name == "DELETE":
                TO_CLEAN.pop()
            return endpoint, "active", TO_CLEAN
        else:
            TO_CLEAN.append(None)
            health_logger.error(f"Error occurred while checking {url}."
                                f"Unexpected response code: {status_code}")
            return endpoint, "inactive", TO_CLEAN
    except Exception as err:
        health_logger.error(f"Error occurred while checking {url}: {err}")
        return endpoint, "inactive", TO_CLEAN
    

async def save_logs(logs: "list[dict[str, list]]"):
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


async def clean_up(table: str, obj_id: str):
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

"""A set of functions to notify a user"""
import requests
from super_admin_1.models.alternative import Database
from super_admin_1.logs.product_action_logger import logger
from super_admin_1.notification.config import url_mapping


class CustomError(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_field_value(field: str, table: str, filter: str, value: str) -> str:
    """Get a particular field value from the db, works for simple get query

    Args:
        field (str): the column on the table you want to get
        table (str): the table in the database
        filter (str): the filtering condition
        value (str): the filtering value

    Returns:
        str: the value from the database
    """
    try:
        query = """SELECT %s FROM %s WHERE %s = %s"""
        with Database() as cursor:
            cursor.execute(query, (field, table, filter, value))
            query_value: str = cursor.fetchone()
        print(type(query_value))
        if query_value is None:
            raise CustomError("A value could not be gotten")
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
        raise CustomError("A value could not be gotten")

    return query_value

def notify(action: str, **kwargs: str) -> dict:
    """Notify of an action

    Args:
        user_id (str): id of the admin user.
        action (str): the action being taken on a shop or products.
        **kwargs (dict): A dictionary of keyword arguments.
    
    Keyword Args:
        product_id (str): id of the product being acted on.
        shop_id (str): id of the shop being acted on.
        reason (str): reason for the action.
    
    Returns:
        dict: To signify success, failure or error
            - success (bool): signifies email sent
            - data (dict): details of the successful mail sent
            - error (bool): signifies error during execution
    """
    email_request_base_url = "https://team-titan.mrprotocoll.me"
    try:
        data: dict = {}
        # update the data dictionary with the available keys
        if kwargs.get("product_id", None):
            product_name, shop_id = get_field_value(field="name, shop_id", table="product",
                                                    filter="id", value=kwargs.get("product_id"))
            data["product_name"] = product_name
            merchant_id = get_field_value(field="merchant_id", table="shop", filter="id", value=shop_id)
        else:
            store_name, merchant_id = get_field_value(field="name, merchant_id", table="shop",
                                        filter="id", value=kwargs.get("shop_id"))
            data["store_name"] = store_name
        if kwargs.get("reason", None):
            data["reason"] = kwargs.get("reason")
        # query the database to get the recipient email
        email, name = get_field_value(field="email, name", table="public.user",
                                      filter="id", value=merchant_id)
        data["recipient"] = email
        data["name"] = name
        
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")

    try:
        endpoint = url_mapping.get(action)
        response = requests.post(f"{email_request_base_url}/{endpoint}", json=data)
        if response.status_code != 200:
            return {
                "success": False,
                "data": {},
                "error": False
            }
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
        return {
            "success": False,
            "data": {},
            "error": True
        }

    return {
        "success": True,
        "data": {
            "recipient": email,
            "name": name,
            "action": action,
            "affected_object": product_name | store_name
        },
        "error": False
    }

def notify_test(name: str, email: str, store_name: str) -> dict:
    
    email_request_url = "https://team-titan.mrprotocoll.me/api/v1/store/suspension-lifted"
    try:
        
        data: dict = {
            "name": name,
            "recipient": email,
            "store_name": store_name,
            # "skill": "Content Writer",
            # "badge_name": "Content Writing",
            # "user_profile_link": "https://example.com"
        }
       
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")

    try:
        response = requests.post(email_request_url, json=data)
        print(f"status code:{response.status_code}")
        if response.status_code != 200:
            return {
                "success": False,
                "error": False
            }
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
        return {
            "success": False,
            "error": True
        }

    return {
        "success": True,
        "error": False
    }

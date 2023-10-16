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
        final_values = []
        if isinstance(field, list):
            for column in field:
                query = f"""SELECT {column} FROM {table} WHERE {filter} = '{value}' """
                with Database() as cursor:
                    cursor.execute(cursor.mogrify(query))
                    query_value: str = cursor.fetchone()
                if query_value is None:
                    raise CustomError("A value could not be gotten")
                final_values.append(query_value[0])
            return final_values
        else:
            query = f"""SELECT {field} FROM {table} WHERE {filter} = '{value}' """
            with Database() as cursor:
                cursor.execute(cursor.mogrify(query))
                query_value: str = cursor.fetchone()
            if query_value is None:
                raise CustomError("A value could not be gotten")
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
        raise CustomError("A value could not be gotten")
    return query_value[0]

def product_action_notification(action: str, **kwargs: str) -> dict:
    """Notify of an action related to a product

    Args:
        action (str): the action being taken on a product.
            - sanction
            - unsanction
            - product deletion
        **kwargs (dict): A dictionary of keyword arguments.

    Keyword Args:
        product_id (str): id of the product being acted on.
        reason (str): reason for the action.

    Returns:
        dict: To signify success, failure or error
            - success (bool): signifies email sent
            - data (dict): details of the successful mail sent
            - error (bool): signifies error during execution
    """
    accepted_action = ["sanction", "unsanction", "product deletion"]
    if action not in accepted_action:
        return False
    email_request_base_url = "https://staging.zuri.team"
    try:
        data: dict = {}
        # update the data dictionary with the available keys
        product_name, shop_id, description = get_field_value(field=["name", "shop_id", "description"],
                                                             table="product", filter="id",
                                                             value=kwargs.get("product_id"))
        data["product_name"] = product_name

        # query the database to get the recipient email and name
        # a comma is added to help in destructuring the tuple (removed already)
        merchant_id = get_field_value(field="merchant_id", table="shop", filter="id", value=shop_id)
        email, name = get_field_value(field=["email", "first_name"], table="public.user",
                                      filter="id", value=merchant_id)
        # get the product image
        url = get_field_value(field="url", table="product_image",
                              filter="product_id", value=kwargs.get("product_id"))
        data["recipient"] = email
        data["name"] = name
        if action != "unsanction":
            data["violation"] = kwargs.get("reason", "Policy violation")
            data["image_url"] = url
            data["product_info"] = description
            if action == "product deletion":
                data["store_link"] = "https://www.not-defined.com"
        else:
            try:
                query = """ SELECT COUNT(*) AS count
                            FROM order_item
                            WHERE product_id = %s
                            GROUP BY product_id;
                        """
                with Database() as cursor:
                    cursor.execute(cursor.mogrify(query, (kwargs.get("product_id"),)))
                    count = cursor.fetchone()
            except Exception as error:
                logger.error(f"{type(error).__name__}: {error}")
            data["sanction_reason"] = kwargs.get("reason", "Policy violation")
            data["product_image_url"] = url
            data["sales_count"] = 0 if count is None else int(count)
            data["store_link"] = "https://www.not-defined.com"
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")

    try:
        endpoint = url_mapping.get(action)
        response = requests.post(f"{email_request_base_url}{endpoint}", json=data)
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
            "affected_object": product_name
        },
        "error": False
    }

def shop_action_notification(action: str, **kwargs: str) -> dict:
    """Notify of an action related to a shop

    Args:
        action (str): the action being taken on a shop.
            - ban
            - unban
            - shop deletion
        **kwargs (dict): A dictionary of keyword arguments.

    Keyword Args:
        shop_id (str): id of the shop being acted on.
        reason (str): reason for the action.

    Returns:
        dict: To signify success, failure or error
            - success (bool): signifies email sent
            - data (dict): details of the successful mail sent
            - error (bool): signifies error during execution
    """
    accepted_action = ["ban", "unban", "shop deletion"]
    if action not in accepted_action:
        return False

    email_request_base_url = "https://staging.zuri.team"
    try:
        data: dict = {}
        # update the data dictionary with the available keys
        store_name, merchant_id = get_field_value(field=["name", "merchant_id"], table="shop",
                                                  filter="id", value=kwargs.get("shop_id"))
        data["store_name"] = store_name

        # query the database to get the recipient email and name
        email, name = get_field_value(field=["email", "name"], table="public.user",
                                      filter="id", value=merchant_id)
        data["recipient"] = email
        data["name"] = name
        if action == "ban":
            data["reason"] = [kwargs.get("reason", "policy violation")]
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")

    try:
        endpoint = url_mapping.get(action)
        response = requests.post(f"{email_request_base_url}{endpoint}", json=data)
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
            "affected_object": store_name
        },
        "error": False
    }

def notify(action: str, **kwargs: str) -> dict:
    """Notify of an action

    Args:
        action (str): the action being taken on a shop or products.
            - ban
            - unban
            - sanction
            - unsanction
            - deletion
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
    accepted_action = ["ban", "unban", "sanction", "unsanction", "deletion"]
    if action not in accepted_action:
        return False

    if not kwargs.get("product_id", None):
        if action == "deletion":
            response = shop_action_notification(action="shop deletion",
                                                reason=kwargs.get("reason", "Policy Violation"),
                                                shop_id=kwargs.get("shop_id"))
            return response
        else:
            response = shop_action_notification(action=action,
                                                reason=kwargs.get("reason", "Policy Violation"),
                                                shop_id=kwargs.get("shop_id"))
            return response
    else:
        if action == "deletion":
            response = product_action_notification(action="product deletion",
                                                   reason=kwargs.get("reason", "Policy Violation"),
                                                   product_id=kwargs.get("product_id"))
            return response
        else:
            response = product_action_notification(action=action,
                                                   reason=kwargs.get("reason", "Policy Violation"),
                                                   product_id=kwargs.get("product_id"))
            return response

def product_action_notification_test(action: str, email: str, **kwargs: str) -> dict:
    """Notify of an action related to a product, same as its original version"""

    accepted_action = ["sanction", "unsanction", "product deletion"]
    if action not in accepted_action:
        return {
            "message": "Invalid action",
            "error": f"{action} is not a valid product action"
        }
    email_request_base_url = "https://staging.zuri.team"
    try:
        data: dict = {}
        # update the data dictionary with the available keys
        product_name, shop_id, description = get_field_value(field=["name", "shop_id", "description"],
                                                             table="product", filter="id",
                                                             value=kwargs.get("product_id"))
        data["product_name"] = product_name

        # query the database to get the recipient email and name
        merchant_id = get_field_value(field="merchant_id", table="shop",
                                      filter="id", value=shop_id)
        name = get_field_value(field="first_name", table="public.user",
                               filter="id", value=merchant_id)
        # get the product image
        url = get_field_value(field="url", table="product_image",
                              filter="product_id", value=kwargs.get("product_id"))
        data["recipient"] = email
        data["name"] = name
        if action != "unsanction":
            data["violation"] = kwargs.get("reason", "Policy violation")
            data["image_url"] = url
            data["product_info"] = description
            if action == "product deletion":
                data["store_link"] = "https://www.not-defined.com"
        else:
            try:
                query = """ SELECT COUNT(*) AS count
                            FROM order_item
                            WHERE product_id = %s
                            GROUP BY product_id;
                        """
                with Database() as cursor:
                    cursor.execute(cursor.mogrify(query, (kwargs.get("product_id"),)))
                    count = cursor.fetchone()
                    # print(f"cursor: {count}")
            except Exception as error:
                logger.error(f"{type(error).__name__}: {error}")
            data["sanction_reason"] = kwargs.get("reason", "Policy violation")
            data["product_image_url"] = url
            data["sales_count"] = 0 if count is None else int(count)
            data["store_link"] = "https://www.not-defined.com"
            # print(f"data: {data}")
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")

    try:
        print(f"data: {data}")
        endpoint = url_mapping.get(action)
        url = f"{email_request_base_url}{endpoint}"
        print(f"url: {url}")
        response = requests.post(url, json=data)
        if response.status_code != 200:
            return response.json()
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
            "affected_object": product_name
        },
        "error": False
    }

def shop_action_notification_test(action: str, email: str, **kwargs: str) -> dict:
    """Notify of an action related to a shop, same as original version"""
    accepted_action = ["ban", "unban", "shop deletion"]
    if action not in accepted_action:
        return {
            "message": "Invalid action",
            "error": f"{action} is not a valid shop action"
        }

    email_request_base_url = "https://staging.zuri.team"
    try:
        data: dict = {}
        # update the data dictionary with the available keys
        store_name, merchant_id = get_field_value(field=["name", "merchant_id"], table="shop",
                                                  filter="id", value=kwargs.get("shop_id"))
        data["store_name"] = store_name

        # query the database to get the recipient email and name
        name = get_field_value(field="first_name", table="public.user",
                               filter="id", value=merchant_id)
        data["recipient"] = email
        data["name"] = name
        if action == "ban":
            data["reason"] = {"reason": kwargs.get("reason", "policy violation")}
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")

    try:
        endpoint = url_mapping.get(action)
        response = requests.post(f"{email_request_base_url}{endpoint}", json=data)
        print(response.json())
        if response.status_code != 200:
            return response.json()
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
            "affected_object": store_name
        },
        "error": False
    }

def notify_test(action: str, email: str, **kwargs: str) -> dict:

    accepted_action = ["ban", "unban", "sanction", "unsanction", "deletion"]
    if action not in accepted_action:
        return False

    if not kwargs.get("product_id", None):
        print("shop")
        print(f"shop_id: {kwargs.get('shop_id')}")
        if action == "deletion":
            response = shop_action_notification_test(action="shop deletion", email=email,
                                                     shop_id=kwargs.get("shop_id"))
            return response
        else:
            response = shop_action_notification_test(action=action, email=email,
                                                     shop_id=kwargs.get("shop_id"))
            return response
    else:
        if action == "deletion":
            response = product_action_notification_test(action="product deletion", email=email,
                                                        product_id=kwargs.get("product_id"))
            return response
        else:
            response = product_action_notification_test(action=action, email=email,
                                                        product_id=kwargs.get("product_id"))
            return response

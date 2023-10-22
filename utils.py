from super_admin_1.errors.handlers import Unauthorized, Forbidden, CustomError
from super_admin_1.logs.product_action_logger import logger
from super_admin_1.models.alternative import Database
from super_admin_1.models.product import Product
from super_admin_1.models.shop import Shop
from types import SimpleNamespace
from typing import Dict, List
from functools import wraps
from uuid import UUID
import requests


def admin_required(request=None):
    """
    A decorator that checks if a user is logged in and has the role of an admin before allowing access to a specific route or function.

    Args:
        request (optional): The request object containing the user's authentication information.

    Returns:
        The decorated function.

    Raises:
        CustomError: If the user is not logged in or does not have the necessary permissions.

    Example Usage:
        @admin_required(request)
        def my_function(user_id):
            # code here
    """
    def super_admin_required(func):
        @wraps(func)
        def get_user_role(*args, **kwargs):
            auth_url = "https://staging.zuri.team/api/auth/api/authorize"
            if not request:
                raise CustomError(error="Unauthorized", code=401,
                                  message="You are not logged in//")
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                raise CustomError(error="Unauthorized", code=401,
                                  message="You are not logged in")
            token = None
            if auth_header.startswith("Bearer"):
                token = auth_header.split(" ")[1]

            response = requests.post(
                auth_url,
                {
                    "token": token,
                    "role": "admin",
                },
            )
            # print("Authentication Service Response:", response.json())

            if response.status_code != 200:
                raise CustomError(error="Bad Request", code=400,
                                  message="Something went wrong while Authenticating this User")

            user_data = response.json()

            if not user_data.get("authorized"):
                raise CustomError(error="Forbidden", code=403,
                                  message="No Permissions to access the requested resource")

            user_id = user_data.get("user")["id"]

            return func(user_id, *args, **kwargs)

        return get_user_role
    return super_admin_required

def image_gen(id: UUID) -> str:
    """
    Retrieves the URL of a product image from a database based on the given product ID.

    Args:
        id (int): The ID of the product for which the image URL needs to be retrieved.

    Returns:
        list: The URL of the product image, if it exists in the database. Otherwise, an empty list is returned.
    """
    product_image = """
        SELECT "url" FROM public.product_image
        WHERE product_id = %s
    """
    image_url = []
    try:
        with Database() as db:
            db.execute(product_image, (id,))
            url = db.fetchall()
        if url:
            return url
    except Exception as e:
        return image_url

def vendor_profile_image(id: UUID) -> str:
    """
    Retrieves the profile picture URL of a user from a database.

    Args:
        id (int): The ID of the user for which the profile picture URL needs to be retrieved.

    Returns:
        str: The profile picture URL of the user with the provided ID.
    """
    user_image = """
        SELECT "profile_pic" FROM public.user
        WHERE id = %s
    """
    image_url = []
    try:
        with Database() as db:
            db.execute(user_image, (id,))
            url = db.fetchone()
        if url:
            pic, = url
            image_url.append(pic)
            return image_url
    except Exception as e:
        return image_url

def vendor_total_order(merchant_id: UUID) -> int:
    """
    Retrieves the total orders of a vendor from the database.

    Args:
        merchant_id (uuid): The merchant_id of the vendor for which the total orders needs to be retrieved.

    Returns:
        int: The total orders count of the vendor with the provided merchant_id.
    """
    order_count = """ 
        SELECT product_id, COUNT(*) AS order_count
        FROM public.order_item
        WHERE merchant_id = %s
        GROUP BY product_id;
    """
    try:
        with Database() as db:
            db.execute(order_count, (merchant_id,))
            result = db.fetchone()
        if result:
            order, = result
            return order
        return 0
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        return 0

def vendor_total_sales(merchant_id: UUID) -> int:
    """
    Retrieves the total sales of a vendor from the database.

    Args:
        merchant_id (uuid): The merchant_id of the vendor for which the total sales needs to be retrieved.

    Returns:
        int: The total sales of the vendor with the provided merchant_id.
    """
    sales_aggregate = """
        SELECT 
        SUM(order_price - order_discount + "order_VAT") AS sales
        FROM public.order_item
        WHERE merchant_id = %s;
    """
    try:
        with Database() as db:
            db.execute(sales_aggregate, (merchant_id,))
            result = db.fetchone()
        if result:
            order, = result
            return order
        return 0
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        return 0

def shop_tuple_to_object(shop_tuple: tuple) -> SimpleNamespace:
    """Convert the shop tuple from direct query to a dictionary

    Args:
        shop_tuple (tuple): the tuple from the cursor
    
    Returns:
        SimpleNamespace: the shop object
    """
    # print(shop_tuple)
    user_dict = {
        "first_name": shop_tuple[12],
        "last_name": shop_tuple[13],
        "email": shop_tuple[14],
        "location": shop_tuple[15],
        "country": shop_tuple[16]
    }
    shop_dict: dict = {
        "id": shop_tuple[0],
        "merchant_id": shop_tuple[1],
        "name": shop_tuple[2],
        "policy_confirmation": shop_tuple[3],
        "restricted": shop_tuple[4],
        "admin_status": shop_tuple[5],
        "is_deleted": shop_tuple[6],
        "reviewed": shop_tuple[7],
        "rating": shop_tuple[8],
        "createdAt": shop_tuple[9],
        "updatedAt": shop_tuple[10],
        "user": SimpleNamespace(**user_dict)
    }
    shop = SimpleNamespace(**shop_dict)
    return shop

def total_shop_count(status: bool = False) -> int:
    """Get the total number of shops"""

    if status:
        query = """
            SELECT COALESCE(SUM(order_price - order_discount + "order_VAT"), 0) AS sales
            FROM shop
            LEFT JOIN public.order_item ON shop.merchant_id = public.order_item.merchant_id
            LEFT JOIN public.user ON shop.merchant_id = public.user.id
            WHERE shop.restricted = 'no' AND shop.is_deleted = 'active'
            GROUP BY shop.id, public.user.id
            ORDER BY sales DESC;
        """
    else:
        query = """
            SELECT COALESCE(SUM(order_price - order_discount + "order_VAT"), 0) AS sales
            FROM shop
            LEFT JOIN public.order_item ON shop.merchant_id = public.order_item.merchant_id
            LEFT JOIN public.user ON shop.merchant_id = public.user.id
            GROUP BY shop.id, public.user.id
            ORDER BY sales DESC;
        """
    try:
        with Database() as cursor:
            cursor.execute(query)
            total = len(cursor.fetchall())
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
        return 0
    return total

def sort_by_top_sales(page: int = 0, status: bool = False) -> List[SimpleNamespace]:
    """A function to filter the shops based on certain query params
    
    Args:
        user_id (string): id of the logged in user
    """
    
    if page == 1:
        page = 0
    else:
        page = (page * 10) - 10

    if status:
        # query to filter by active status
        query = """
            SELECT shop.*, COALESCE(SUM(order_price - order_discount + "order_VAT"), 0) AS sales, public.user.first_name, 
            public.user.last_name, public.user.email, public.user.location, public.user.country
            FROM shop
            LEFT JOIN public.order_item ON shop.merchant_id = public.order_item.merchant_id
            LEFT JOIN public.user ON shop.merchant_id = public.user.id
            WHERE shop.restricted = 'no' AND shop.is_deleted = 'active'
            GROUP BY shop.id, public.user.id
            ORDER BY sales DESC
            LIMIT 10 OFFSET %s;
        """
    else:
        # query to filter generally by top sales
        query = """
            SELECT shop.*, COALESCE(SUM(order_price - order_discount + "order_VAT"), 0) AS sales, public.user.first_name, 
            public.user.last_name, public.user.email, public.user.location, public.user.country
            FROM shop
            LEFT JOIN public.order_item ON shop.merchant_id = public.order_item.merchant_id
            LEFT JOIN public.user ON shop.merchant_id = public.user.id
            GROUP BY shop.id, public.user.id
            ORDER BY sales DESC
            LIMIT 10 OFFSET %s;
        """
    try:
        with Database() as cursor:
            cursor.execute(query, (page,))
            shops = cursor.fetchall()
            # print(shops)
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
        return []


    try:
        return [shop_tuple_to_object(shop) for shop in shops]
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
        return []

def check_shop_status(shop: Shop) -> str:
    """
    Check the status of a shop.

    Args:
        shop: The shop object to check the status for.

    Returns:
        str: The status of the shop. Possible values are "Banned", "Active", or "Deleted".

    Examples:
        # Example 1: Check the status of a shop
        status = check_status(shop)
    """

    if (
        shop.admin_status in ["suspended", "blacklisted"]
        and shop.restricted == "temporary"
    ):
        return "Banned"
    if (
        shop.admin_status in ["approved", "pending"]
        and shop.restricted == "no"
        and shop.is_deleted == "active"
    ):
        return "Active"
    if shop.is_deleted == "temporary":
        return "Deleted"

def check_product_status(product: Product) -> str:
    if product.admin_status in ["suspended", "blacklisted"]:
        return "Sanctioned"
    elif (
        product.admin_status == "approved"
        and product.is_deleted == "active"
    ):
        return "Active"
    elif (
        product.admin_status == "pending"
        and product.is_deleted == "active"
    ):
        return "Pending"
    elif product.is_deleted == "temporary":
        return "Deleted"

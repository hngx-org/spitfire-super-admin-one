from functools import wraps
from super_admin_1.errors.handlers import Unauthorized, Forbidden, CustomError
import requests
from super_admin_1.models.alternative import Database


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


def raise_validation_error(error):
    msg = []
    for err in error.errors():
        msg.append({
            "field": err["loc"][0],
            "error": err["msg"]
        })
    raise CustomError("Bad Request", 400, "Input should be a valid UUID")


def image_gen(id):
    """
    Retrieves the URL of a product image from a database based on the given product ID.

    Args:
        id (int): The ID of the product for which the image URL needs to be retrieved.

    Returns:
        list: The URL of the product image, if it exists in the database. Otherwise, an empty list is returned.
    """
    product_image = """
                    SELECT "url" FROM public.product_image
                    WHERE product_id = %s"""
    image_url = []
    try:
        with Database() as db:
            db.execute(product_image, (id,))
            url = db.fetchall()
        if url:
            return url
    except Exception as e:
        return image_url


def vendor_profile_image(id):
    """
    Retrieves the profile picture URL of a user from a database.

    Args:
        id (int): The ID of the user for which the profile picture URL needs to be retrieved.

    Returns:
        str: The profile picture URL of the user with the provided ID.
    """
    user_image = """
                    SELECT "profile_pic" FROM public.user
                    WHERE id = %s"""
    image_url = []
    try:
        with Database() as db:
            db.execute(user_image, (id,))
            url = db.fetchone()
        if url:
            return url
    except Exception as e:
        return image_url


def vendor_total_order(merchant_id):
    """
    Retrieves the total orders of a vendor from the database.

    Args:
        merchant_id (uuid): The merchant_id of the vendor for which the total orders needs to be retrieved.

    Returns:
        int: The total orders count of the vendor with the provided merchant_id.
    """
    order_count = """ SELECT COUNT(*) AS count, * 
                        FROM public.OrderItem 
                        WHERE merchant_id = %s;
                   """
    orders = []
    try:
        with Database() as db:
            db.execute(order_count, (merchant_id,))
            url = db.fetchall()
        if url:
            return url
    except Exception as e:
        return orders


def vendor_total_sales(merchant_id):
    """
    Retrieves the total sales of a vendor from the database.

    Args:
        merchant_id (uuid): The merchant_id of the vendor for which the total sales needs to be retrieved.

    Returns:
        int: The total sales of the vendor with the provided merchant_id.
    """
    sales_aggregate = """SUM(order_price - order_discount + order_VAT) AS sales
            FROM OrderItem
            WHERE merchant_id = %s;
                   """
    sales = []
    try:
        with Database() as db:
            db.execute(sales_aggregate, (merchant_id,))
            url = db.fetchall()
        if url:
            return url
    except Exception as e:
        return sales

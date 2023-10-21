from flask import Blueprint, jsonify, request
from super_admin_1.models.alternative import Database
from super_admin_1 import db
from super_admin_1.models.shop import Shop
from super_admin_1.models.product import Product
from super_admin_1.shop.shoplog_helpers import ShopLogs
from super_admin_1.notification.notification_helper import notify
from super_admin_1.logs.product_action_logger import logger
from sqlalchemy.exc import SQLAlchemyError
from super_admin_1.shop.shop_schemas import IdSchema
from pydantic import ValidationError
from utils import raise_validation_error, admin_required, sort_by_top_sales, total_shop_count
from utils import admin_required, image_gen, vendor_profile_image, vendor_total_order, vendor_total_sales
from collections import defaultdict
from super_admin_1 import cache
from typing import Dict, List
from uuid import UUID
import os

import uuid


shop = Blueprint("shop", __name__, url_prefix="/api/v1/admin/shops")



# TEST - Documented
@shop.route("/endpoint", methods=["GET"])
@admin_required(request=request)
def shop_endpoint(user_id : UUID) -> dict:
    """
    Handle GET requests to the shop endpoint.

    Returns:
        jsonify: A JSON response indicating the success of the request.
    """
    response_data = {
        "message": f"This is the shop endpoint under /api/shop/endpoint {user_id}"}
    return jsonify(response_data), 200


@shop.route("/all", methods=["GET"])
@admin_required(request=request)
def get_shops(user_id : UUID) -> dict:
    """
Get all shops information.

Args:
    user_id (UUID): The ID of the user.

Returns:
    dict: A dictionary containing the following information:
        - "message" (str): The message indicating the success of the operation.
        - "data" (list): A list of dictionaries containing the details of each shop.
        - "total_shops" (int): The total count of all shops.
        - "total_banned_shops" (int): The total count of banned shops.
        - "total_deleted_shops" (int): The total count of deleted shops.
        - "total_pages" (int): The total number of pages.

Raises:
    Exception: If there is an error during the retrieval process.

Examples:
    # Example 1: Get all shops information
    get_shops(user_id)
"""
  
    page = request.args.get('page', 1, int)
    search = request.args.get('search', None, str)
    status = request.args.get('status', None, str)


    statuses = {
        "active": ["pending", "approved"],
        "banned": ["temporary"],
        "deleted": ["temporary"]
    }
    status_enum = {
        "active": "admin_status",
        "banned": "restricted",
        "deleted": "is_deleted"
    }
    admin_status = {
        "active": ["pending", "approved"],
        "banned": ["suspended", "blacklisted"],
        "deleted": ["pending", "approved", "reviewed"] 
    }


    try:
        if status and search:
            shops = Shop.query.filter(
                Shop.name.ilike(f'%{search}%'),
                Shop.admin_status.in_(admin_status[status]),
                getattr(Shop, status_enum[status]).in_(statuses[status])
            ).order_by(Shop.createdAt.desc()).paginate(page=page, per_page=10, error_out=False)

        elif status:
            shops = Shop.query.filter(
                Shop.admin_status.in_(admin_status[status]),
                getattr(Shop, status_enum[status]).in_(statuses[status])
            ).order_by(Shop.createdAt.desc()).paginate(page=page, per_page=10, error_out=False)  

        elif search:
            shops = Shop.query.filter(Shop.name.ilike(f'%{search}%')).order_by(Shop.createdAt.desc()).paginate(page=page, per_page=10, error_out=False)

        else:
            shops = sort_by_top_sales(page=page)
        data = []
    except Exception as error:
        return jsonify({
            "message": "Bad Request",
            "error": f"{error} is not recognized"
        })

    def check_status(shop: Shop):
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

    if isinstance(shops, list):
        total_shops = total_shop_count()
        total_no_of_pages = total_shops / 10
        total_remainder = total_shops % 10
        if total_remainder > 0:
            total_no_of_pages += 1
    else:
        total_shops = Shop.query.count()
        total_no_of_pages = shops.pages
    banned_shops = Shop.query.filter(Shop.admin_status.in_(['suspended', 'blacklisted']), Shop.restricted == 'temporary').count()
    deleted_shops = Shop.query.filter_by(is_deleted="temporary").count()

    try:
        for shop in shops:
            total_products = Product.query.filter_by(shop_id=shop.id).count()
            merchant_name = f"{shop.user.first_name} {shop.user.last_name}"
            joined_date = shop.createdAt.strftime("%d-%m-%Y")
            shop_data = {
                "vendor_id": shop.id,
                "vendor_name": shop.name,
                "merchant_id": shop.merchant_id,
                "merchant_name": merchant_name,
                "merchant_email": shop.user.email,
                "merchant_location": shop.user.location,
                "merchant_country": shop.user.country,
                "vendor_profile_pic": vendor_profile_image(shop.merchant_id),
                "policy_confirmation": shop.policy_confirmation,
                "restricted": shop.restricted,
                "admin_status": shop.admin_status,
                "is_deleted": shop.is_deleted,
                "reviewed": shop.reviewed,
                "rating": shop.rating,
                "createdAt": shop.createdAt,
                "joined_date": joined_date,
                "updatedAt": shop.updatedAt,
                "vendor_status": check_status(shop),
                "total_products": total_products,
            }
            data.append(shop_data)
        return jsonify(
            {
                "message": "all shops information", 
                "data": data, 
                "total_shops": total_shops,
                "total_banned_shops": banned_shops, 
                "total_deleted_shops": deleted_shops,
                "total_pages": int(total_no_of_pages)
                }
                ), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@shop.route("/total-sales", methods=["POST"])
@admin_required(request=request)
def total_shop_sales(user_id : UUID) -> defaultdict:
    """
Get the total sales and orders for multiple shops.

Args:
    user_id (UUID): The ID of the user.

Returns:
    defaultdict: A defaultdict containing the total sales and orders for each shop.
        The keys of the defaultdict are the merchant IDs (str), and the values are lists containing the sales and orders.
        If a merchant ID is not valid or not found in the shop table, it will be skipped.

Examples:
    # Example 1: Get the total sales and orders for multiple shops
    total_shop_sales(user_id)
"""

    total = defaultdict(list)
    req_data = request.get_json()
    merchant_id_list = req_data.get("merchants", None)
    if not merchant_id_list and isinstance(merchant_id_list, list):
        return jsonify(
            {
                "error": "Invalid payload format.",
                "message": "Bad input format",
            }
        ), 400
    for merchant in merchant_id_list:
        #NEED TO VERIFY THE MERCHANT_ID IS A VALID UUID
        try:
            merchant = IdSchema(id=merchant)
            merchant = merchant.id
        except ValidationError as e:
            continue

                # TO VALIDATE IT IS IN THE SHOP TABLE
        try:
            c = Shop.query.filter_by(merchant_id=merchant).first()
            if not c:
                continue
            total_sales = total.__getitem__(str(merchant))
            sales = vendor_total_sales(c.merchant_id)
            orders = vendor_total_order(c.merchant_id)
            total_sales.append(sales)
            total_sales.append(orders)
        except Exception as exc:
            return jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "something went wrong"
                }
            ), 500
    return jsonify(
        {
            "message": "total Sales and Order Retrieved",
            "data":total
        }
    ), 200


@shop.route("/<shop_id>", methods=["GET"])
@admin_required(request=request)
def get_shop(user_id : UUID, shop_id : UUID) -> dict:
    """
Get the information of a shop.

Args:
    user_id (UUID): The ID of the user.
    shop_id (UUID): The ID of the shop to retrieve information for.

Returns:
    dict: A dictionary containing the information of the shop:
        - "vendor_id" (UUID): The ID of the shop.
        - "vendor_name" (str): The name of the shop.
        - "merchant_id" (UUID): The ID of the merchant.
        - "vendor_profile_pic" (str): The profile picture of the vendor.
        - "merchant_name" (str): The name of the merchant.
        - "merchant_email" (str): The email of the merchant.
        - "merchant_location" (str): The location of the merchant.
        - "merchant_country" (str): The country of the merchant.
        - "vendor_total_orders" (int): The total number of orders for the vendor.
        - "vendor_total_sales" (float): The total sales amount for the vendor.
        - "policy_confirmation" (bool): The confirmation status of the shop's policy.
        - "restricted" (str): The restriction status of the shop.
        - "admin_status" (str): The administrative status of the shop.
        - "is_deleted" (str): The deletion status of the shop.
        - "reviewed" (bool): The review status of the shop.
        - "rating" (float): The rating of the shop.
        - "createdAt" (datetime): The creation date of the shop.
        - "joined_date" (str): The formatted joined date of the shop.
        - "updatedAt" (datetime): The last update date of the shop.
        - "vendor_status" (str): The status of the shop based on its administrative and deletion status.
        - "products" (list): A list of dictionaries containing the information of each product in the shop.
            - "product_image" (str): The image of the product.
            - "product_id" (UUID): The ID of the product.
            - "product_rating_id" (UUID): The ID of the product rating.
            - "category_id" (UUID): The ID of the category.
            - "category_name" (str): The name of the category.
            - "sub_category_name" (str): The name of the sub-category.
            - "product_name" (str): The name of the product.
            - "description" (str): The description of the product.
            - "quantity" (int): The quantity of the product.
            - "price" (float): The price of the product.
            - "discount_price" (float): The discounted price of the product.
            - "tax" (float): The tax amount of the product.
            - "product_admin_status" (str): The administrative status of the product.
            - "product_is_deleted" (str): The deletion status of the product.
            - "product_is_published" (bool): The publication status of the product.
            - "currency" (str): The currency of the product.
            - "createdAt" (datetime): The creation date of the product.
            - "updatedAt" (datetime): The last update date of the product.
            - "product_status" (str): The status of the product based on its administrative and deletion status.
            - "product_date_added" (str): The formatted date when the product was added.

Raises:
    Exception: If there is an error during the retrieval process.

Examples:
    # Example 1: Get the information of a shop
    get_shop(user_id, shop_id)
"""

    shop_id = IdSchema(id=shop_id)
    shop_id = shop_id.id
    shop = Shop.query.filter_by(id=shop_id).first()
    data = []

    if not shop:
        return jsonify({"error": "not found", "message": "invalid shop id"}), 404

    def check_status(shop):
        if shop.admin_status == "suspended" and shop.restricted == "temporary":
            return "Banned"
        if (
            shop.admin_status in ["approved", "pending"]
            and shop.restricted == "no"
            and shop.is_deleted == "active"
        ):
            return "Active"
        if shop.is_deleted == "temporary":
            return "Deleted"

    def check_product_status(product):
        if product.admin_status == "suspended":
            return "Sanctioned"
        if (
            product.admin_status == "approved"
            and product.is_deleted == "active"
        ):
            return "Active"
        if (
            product.admin_status == "pending"
            and product.is_deleted == "active"
        ):
            return "Pending"
        if product.is_deleted == "temporary":
            return "Deleted"

    try:
        page = request.args.get('page',1 , int)
        products = Product.query.filter_by(shop_id=shop.id).paginate(page=page,per_page=10,error_out=False)
        total_products = products.total
        total_pages=products.pages
        merchant_name = f"{shop.user.first_name} {shop.user.last_name}"
        joined_date = shop.createdAt.strftime("%d-%m-%Y")
        shop_data = {
            "vendor_id": shop.id,
            "vendor_name": shop.name,
            "merchant_id": shop.merchant_id,
            "vendor_profile_pic": vendor_profile_image(shop.merchant_id),
            "merchant_name": merchant_name,
            "merchant_email": shop.user.email,
            "merchant_location": shop.user.location,
            "merchant_country": shop.user.country,
            "vendor_total_orders": vendor_total_order(shop.merchant_id),
            "vendor_total_sales": vendor_total_sales(shop.merchant_id),
            "policy_confirmation": shop.policy_confirmation,
            "restricted": shop.restricted,
            "admin_status": shop.admin_status,
            "is_deleted": shop.is_deleted,
            "reviewed": shop.reviewed,
            "rating": shop.rating,
            "createdAt": shop.createdAt,
            "joined_date": joined_date,
            "updatedAt": shop.updatedAt,
            "vendor_status": check_status(shop),
            "products": [{
                "product_image": image_gen(product.id),
                "product_id": product.id,
                "product_rating_id": product.rating_id,
                "category_id": product.category_id,
                "category_name": product.product_category.name,
                "sub_category_name": product.product_category.product_sub_categories[0].name if product.product_category.product_sub_categories else None,
                "product_name": product.name,
                "description": product.description,
                "quantity": product.quantity,
                "price": product.price,
                "discount_price": product.discount_price,
                "tax": product.tax,
                "product_admin_status": product.admin_status,
                "product_is_deleted": product.is_deleted,
                "product_is_published": product.is_published,
                "currency": product.currency,
                "createdAt": product.createdAt,
                "updatedAt": product.updatedAt,
                "product_status": check_product_status(product),
                "product_date_added": product.createdAt.strftime("%d-%m-%Y")
            } for product in products if products]
        }
        data.append(shop_data)
        return jsonify(
            {"message": "the shop information",
             "data": data,
             "total_pages":total_pages,
             "total_products":total_products
             }
             ), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500



@shop.route("/<shop_id>/ban", methods=["PUT"])
@admin_required(request=request)
def ban_vendor(user_id : UUID, shop_id : UUID) -> dict:
    """
Ban a vendor temporarily.

Args:
    user_id (UUID): The ID of the user.
    shop_id (UUID): The ID of the vendor to ban.

Returns:
    dict: A dictionary containing the following information:
        - "message" (str): The message indicating the success of the operation.
        - "reason" (str): The reason for the vendor ban.
        - "data" (dict): A dictionary containing the details of the banned vendor:
            - "id" (UUID): The ID of the vendor.
            - "merchant_id" (UUID): The ID of the merchant.
            - "name" (str): The name of the vendor.
            - "policy_confirmation" (bool): The confirmation status of the vendor's policy.
            - "restricted" (str): The restriction status of the vendor.
            - "admin_status" (str): The administrative status of the vendor.
            - "is_deleted" (str): The deletion status of the vendor.
            - "reviewed" (bool): The review status of the vendor.
            - "rating" (float): The rating of the vendor.
            - "created_at" (str): The creation date of the vendor.
            - "updated_at" (str): The last update date of the vendor.
            - "products" (list): A list of dictionaries containing the details of each product of the vendor:
                - "id" (UUID): The ID of the product.
                - "name" (str): The name of the product.
                - "description" (str): The description of the product.
                - "admin_status" (str): The administrative status of the product.
                - "price" (float): The price of the product.

Raises:
    ValidationError: If there is a validation error.
    Exception: If there is an error during the banning process.

Examples:
    # Example 1: Ban a vendor temporarily
    ban_vendor(user_id, vendor_id)
"""

    vendor_id = IdSchema(id=vendor_id)
    vendor_id = vendor_id.id
    try:
        # Check if the vendor is already banned
        check_query = """
            SELECT "restricted" FROM "shop"
            WHERE "id" = %s
        """
        with Database() as cursor:
            cursor.execute(check_query, (vendor_id,))
            current_state = cursor.fetchone()

        if current_state and current_state[0] == "temporary":
            return jsonify(
                {
                    "error": "Conflict",
                    "message": "Action already carried out on this Shop",
                }
            ), 409
        # Extract the reason from the request payload
        reason = None
        if request.headers.get("Content-Type") == "application/json":
            try:
                data = request.get_json()
                reason = data.get("reason")
            except Exception as e:
                pass

        # Proceed with banning the vendor
        update_query = """
            UPDATE "shop"
            SET "restricted" = 'temporary', 
                "admin_status" = 'suspended',
                "updatedAt" = current_timestamp
            WHERE "id" = %s
            RETURNING *;  -- Return the updated row
        """
        with Database() as cursor:
            cursor.execute(update_query, (vendor_id,))
            updated_vendor = cursor.fetchone()

        # Inside the ban_vendor function after fetching updated_vendor data
        if updated_vendor:

            cascade_ban_query = """ 
                UPDATE "product"
                SET "admin_status" = 'suspended',
                    "updatedAt" = current_timestamp
                WHERE "shop_id" = %s AND "is_deleted" != 'temporary'
                RETURNING "id", "name", "description", "admin_status", "price";
            """
            with Database() as cursor:
                cursor.execute(cascade_ban_query, (vendor_id,))
                updated_products = cursor.fetchall()

            vendor_details = {
                "id": updated_vendor[0],
                "merchant_id": updated_vendor[1],
                "name": updated_vendor[2],
                "policy_confirmation": updated_vendor[3],
                "restricted": updated_vendor[4],
                "admin_status": updated_vendor[5],
                "is_deleted": updated_vendor[6],
                "reviewed": updated_vendor[7],
                "rating": float(updated_vendor[8]) if updated_vendor[8] is not None else None,
                "created_at": str(updated_vendor[9]),
                "updated_at": str(updated_vendor[10]),
                "products": [{
                    "id": product[0],
                    "name": product[1],
                    "description": product[2],
                    "admin_status": product[3],
                    "price": product[4]
                } for product in updated_products if len(updated_products) > 0]
            }
            # ===================notify vendor of ban action=======================
            try:
                notify("ban", shop_id=vendor_id)
            except Exception as error:
                logger.error(f"{type(error).__name__}: {error} - stacktrace: {os.getcwd()}")
            # ======================================================================
            return jsonify({
                "message": "Vendor account banned temporarily.",
                "reason": reason,
                "data": vendor_details
            }), 201
        else:
            return jsonify(
                {
                    "error": "Not Found",
                    "message": "Vendor not found."
                }
            ), 404
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e} - stacktrace: {os.getcwd()}")
        return jsonify(
            {
                "error": "Internal Server Error",
                "message": "something went wrong"
            }
        ), 500


@shop.route("/<shop_id>/unban", methods=["PUT"])
@admin_required(request=request)
def unban_vendor(user_id: UUID, shop_id : UUID) -> dict:
    """
Unban a vendor.

Args:
    user_id (UUID): The ID of the user.
    shop_id (UUID): The ID of the vendor to unban.

Returns:
    dict: A dictionary containing the following information:
        - "message" (str): The message indicating the success of the operation.
        - "vendor_details" (dict): A dictionary containing the details of the unbanned vendor:
            - "id" (UUID): The ID of the vendor.
            - "merchant_id" (UUID): The ID of the merchant.
            - "name" (str): The name of the vendor.
            - "policy_confirmation" (bool): The confirmation status of the vendor's policy.
            - "restricted" (str): The restriction status of the vendor.
            - "admin_status" (str): The administrative status of the vendor.
            - "is_deleted" (str): The deletion status of the vendor.
            - "reviewed" (bool): The review status of the vendor.
            - "rating" (float): The rating of the vendor.
            - "created_at" (str): The creation date of the vendor.
            - "updated_at" (str): The last update date of the vendor.
            - "products" (list): A list of dictionaries containing the details of each product of the vendor:
                - "id" (UUID): The ID of the product.
                - "name" (str): The name of the product.
                - "admin_status" (str): The administrative status of the product.

Raises:
    ValidationError: If there is a validation error.
    Exception: If there is an error during the unbanning process.

Examples:
    # Example 1: Unban a vendor
    unban_vendor(user_id, shop_id)
"""



    shop_id = IdSchema(id=shop_id)
    shop_id = shop_id.id
    try:
    

        # Search the database for the vendor with the provided vendor_id
        vendor = Shop.query.filter_by(id=shop_id).first()
        if not vendor:
            return jsonify(
                {
                    "Error": "Not Found",
                    "message": "Vendor not found."
                }
            ), 404

        # Check if the vendor is already unbanned
        if vendor.restricted == "no":
            return jsonify(
                {"Error": "Conflict",
                    "message": "This Vendor is Not Banned"}
            ), 409

        vendor.restricted = "no"
        vendor.admin_status = "approved"
        vendor.is_deleted = "active"

        vendor.update()

        vendor_products = Product.query.filter_by(shop_id=shop_id).all()
        products = []
        for product in vendor_products:
            product.admin_status = "approved"
            product.update()
            products.append(product.format())


        # Construct vendor details for the response
        vendor_details = {
            "id": vendor.id,
            "merchant_id": vendor.merchant_id,
            "name": vendor.name,
            "policy_confirmation": vendor.policy_confirmation,
            "restricted": vendor.restricted,
            "admin_status": vendor.admin_status,
            "is_deleted": vendor.is_deleted,
            "reviewed": vendor.reviewed,
            "rating": float(vendor.rating) if vendor.rating is not None else None,
            "created_at": str(vendor.createdAt),
            "updated_at": str(vendor.updatedAt),
            "products": products
        }
        try:
            notify("unban", shop_id=shop_id)
        except Exception as error:
            logger.error(f"{type(error).__name__}: {error} - stacktrace: {os.getcwd()}")

        # Return a success message
        return jsonify(
                {
                    "message": "Vendor unbanned successfully.",
                    "vendor_details": vendor_details,
                }
            ), 200
    except SQLAlchemyError as e:
        # If an error occurs during the database operation, roll back the transaction
        db.session.rollback()
    except Exception as error:
        logger.error(f"{type(e).__name__}: {e}")
        return jsonify({"status": "Error.", "message": str(e)}), 500




@shop.route("/<shop_id>/restore", methods=["PATCH"])
@admin_required(request=request)
def restore_shop(user_id : UUID, shop_id : UUID) -> dict:
    """
Restore a shop.

Args:
    user_id (UUID): The ID of the user.
    shop_id (UUID): The ID of the shop to restore.

Returns:
    dict: A dictionary containing the following information:
        - "message" (str): The message indicating the success of the operation.
        - "data" (dict): A dictionary containing the details of the restored shop.

Raises:
    ValidationError: If there is a validation error.
    Exception: If there is an error during the restoration process.

Examples:
    # Example 1: Restore a shop
    restore_shop(user_id, shop_id)
"""
    shop_id = IdSchema(id=shop_id)
    shop_id = shop_id.id
    try:
        shop = Shop.query.filter_by(id=shop_id).first()
    except Exception as e:
        if not shop:
            return jsonify({"Error": "Not Found", "Message": "Shop Not Found"}), 404

    # change the object attribute from temporary to active
    if shop.is_deleted == "temporary":
        shop.is_deleted = "active"
        shop.admin_status = "approved"
        shop.resticted = "no"
        try:
            db.session.commit()

            """
            The following logs the action in the shop_log db
            """
            get_user_id = shop.user.id
            action = ShopLogs(shop_id=shop_id, user_id=get_user_id)
            action.log_shop_deleted(delete_type="active")

            return (
                jsonify(
                    {"message": "shop restored successfully", "data": shop.format()}
                ),
                201,
            )
        except Exception as e:
            return jsonify(
                {
                    "Error": "Internal Server Error",
                    "message": str(e),
                }
            )
    else:
        return (
            jsonify(
                {
                    "error": "Conflict",
                    "message": "Action already carried out on this Shop",
                }
            ),
            409,
        )


@shop.route("/<shop_id>/soft-delete", methods=["PATCH"])
@admin_required(request=request)
def delete_shop(user_id : UUID, shop_id : UUID) -> dict:
    """
Delete a shop temporarily.

Args:
    user_id (UUID): The ID of the user.
    shop_id (UUID): The ID of the shop to delete.

Returns:
    dict: A dictionary containing the following information:
        - "message" (str): The message indicating the success of the operation.
        - "reason" (str): The reason for the temporary deletion.
        - "data" (None): The data is set to None.

Raises:
    ValidationError: If there is a validation error.
    Exception: If there is an error during the deletion process.

Examples:
    # Example 1: Delete a shop temporarily
    delete_shop(user_id, shop_id)
"""
    shop_id = IdSchema(id=shop_id)
    shop_id = shop_id.id
    # verify if shop exists
    shop = Shop.query.filter_by(id=shop_id).first()
    if not shop:
        return jsonify({"error": "Not Found", "message": "Shop not found"}), 404
    # check if shop is temporary
    if shop.is_deleted == "temporary":
        return (
            jsonify(
                {
                    "error": "Conflict",
                    "message": "Action already carried out on this Shop",
                }
            ),
            409,
        )
    # unban before deleting
    if shop.restricted == "temporary" and shop.admin_status == 'suspended':
        shop.restricted = "no"
        shop.admin_status = 'approved'
    reason = None
    if request.headers.get("Content-Type") == "application/json":
        try:
            data = request.get_json()
            reason = data.get("reason")
        except Exception as e:
            pass

    # delete shop temporarily
    shop.is_deleted = "temporary"
    # Cascade the temporary delete action to associated products
    products = Product.query.filter_by(shop_id=shop_id).all()
    for product in products:
        product.is_deleted = 'temporary'
        db.session.add(product)

    db.session.commit()

    """
    The following logs the action in the shop_log db
    """
    get_user_id = shop.user.id
    action = ShopLogs(shop_id=shop_id, user_id=get_user_id)
    action.log_shop_deleted(delete_type="temporary")
    # ================notify deletion==========================
    try:
        notify("deletion", shop_id=shop_id, reason=reason)
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
    # =========================================================
    return jsonify(
        {'message': "Shop and associated products temporarily deleted",
         "reason": reason,
         "data": None,
         }), 204


@shop.route("/<shop_id>", methods=["DELETE"])
@admin_required(request=request)
def permanent_delete(user_id : UUID, shop_id : UUID) -> None:
    """
Permanently delete a shop and its associated products.

Args:
    user_id (UUID): The ID of the user.
    shop_id (UUID): The ID of the shop to delete.

Returns:
    None

Raises:
    ValidationError: If there is a validation error.
    Exception: If there is an error during the deletion process.

Examples:
    # Example 1: Permanently delete a shop and its associated products
    permanent_delete(user_id, shop_id)
"""   
    shop_id = IdSchema(id=shop_id)
    shop_id = shop_id.id
    try:
        shop = Shop.query.filter_by(id=shop_id).first()
        if not shop:
            return jsonify(
                {
                    "error": "Not Found",
                    'message': 'Shop not found'
                }
            ), 400
        # access associated products
        products = Product.query.filter_by(shop_id=shop_id).all()
        # access reviews for each product and delete them one by one
        for product in products:
            db.session.delete(product)
            db.session.commit()

        db.session.delete(shop)
        db.session.commit()
        # ================notify deletion==========================
        try:
            notify("deletion", shop_id=shop_id)
        except Exception as error:
            logger.error(f"{type(error).__name__}: {error}")
        # =========================================================
        return jsonify({'message': 'Shop and associated products deleted permanently'}), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500




















































# @shop.route("/temporarily-deleted-vendors", methods=["GET"])
# @admin_required(request=request)
# def get_temporarily_deleted_vendors(user_id):
#     """
#     Retrieve temporarily deleted vendors.

#     This endpoint allows super admin users to retrieve a list of vendors who have been temporarily deleted.

#     Returns:
#         JSON response with status and message:
#         - Success (HTTP 200): A list of temporarily deleted vendors and their details.
#         - Success (HTTP 200): A message indicating that no vendors have been temporarily deleted.
#         - Error (HTTP 500): If an error occurs during the retrieving process.

#     Permissions:
#         - Only accessible to super admin users.

#     Note:
#         - The list includes the details of vendors who have been temporarily deleted.
#         - If no vendors have been temporarily deleted, a success message is returned.
#     """
#     try:
#         # Query the database for all temporarily_deleted_vendors
#         temporarily_deleted_vendors = Shop.query.filter_by(
#             is_deleted="temporary").all()

#         # Calculate the total count of temporarily deleted vendors
#         total_count = len(temporarily_deleted_vendors)

#         # Check if no vendors have been temporarily deleted
#         if not temporarily_deleted_vendors:
#             return jsonify(
#                 {
#                     "message": "No vendors have been temporarily deleted",
#                     "data": total_count,
#                 }
#             ), 200

#         # Create a list with vendors details
#         vendors_list = [vendor.format()
#                         for vendor in temporarily_deleted_vendors]

#         # Return the list with all attributes of the temporarily_deleted_vendors
#         return jsonify(
#             {
#                 "message": "All temporarily deleted vendors retrieved successfully",
#                 "data": {
#                     "temporarily_deleted_vendors": vendors_list,
#                     "count": total_count,
#                 }
#             }
#         ), 200
#     except Exception as e:
#         # Handle any exceptions that may occur during the retrieving process
#         return jsonify({"status": "Error", "message": str(e)})


# # Define a route to get details of a temporarily deleted vendor based on his/her ID
# @shop.route("/temporarily-deleted-vendor/<string:vendor_id>",  methods=["GET"])
# # WORKS - Documented
# @admin_required(request=request)
# def get_temporarily_deleted_vendor(user_id, vendor_id):
#     """
#     Retrieve details of a temporarily deleted vendor based on its ID.

#     Args:
#         vendor_id (string): The unique identifier of the vendor to retrieve.

#     Returns:
#         JSON response with status and message:
#         - Success (HTTP 200): Details of the temporarily deleted vendor.
#         - Error (HTTP 404): If the vendor with the provided ID is not found or not temporarily deleted.
#         - Error (HTTP 500): If an error occurs during the retrieval process.

#     Permissions:
#         - Only accessible to super admin users.

#     Note:
#         - This endpoint allows super admin users to retrieve the details of a temporarily deleted vendor based on his/her ID.
#     """
#     try:
#         try:
#             vendor_id = IdSchema(id=vendor_id)
#             vendor_id = vendor_id.id
#         except ValidationError as e:
#             raise_validation_error(e)

#         # Query the database for the vendor with the provided vendor_id that is temporarily deleted
#         temporarily_deleted_vendor = Shop.query.filter_by(
#             id=vendor_id, is_deleted="temporary"
#         ).first()

#         # If the vendor with the provided ID doesn't exist or is not temporarily deleted, return a 404 error
#         if not temporarily_deleted_vendor:
#             return jsonify(
#                 {
#                     "Error": " Not Found",
#                     "message": "vendor not found.",
#                 }
#             ),  404

#         # Return the details of the temporarily deleted vendor
#         vendor_details = temporarily_deleted_vendor.format()

#         return jsonify(
#             {
#                 "message": "Temporarily deleted vendor details retrieved successfully",
#                 "data": vendor_details,
#             }
#         ), 200

#     except SQLAlchemyError as e:
#         # Handle any exceptions that may occur during the retrieval process
#         db.session.rollback()
#         return jsonify({"status": "Error", "message": str(e)}), 500


# # WORKS - Documented
# @shop.route("/sanctioned", methods=["GET"])
# @admin_required(request=request)
# def sanctioned_shop(user_id):
#     """
#     Get all sanctioned products from the database.

#     Args:
#       None

#     Returns:
#       A JSON response containing a message and a list of dictionary objects representing the sanctioned shop.
#       If no shop are found, the message will indicate that and the object will be set to None.
#     """
#     data = []
#     # get all the product object, filter by is_delete = temporay and rue and admin_status = "suspended"
#     query = Shop.query.filter(
#         Shop.admin_status == "suspended",
#     ).all()

#     # if the query is empty
#     if not query:
#         return jsonify({
#             "error": "Not Found",
#             "message": "No shops found",
#         }), 404

#     # populate the object to a list of dictionary object
#     for obj in query:
#         data.append(obj.format())
#     return jsonify({
#         "message": "All sanctioned shops",
#         "object": data
#     }), 200



@shop.route("/all/filters", methods=["GET"])
@admin_required(request=request)
def filters(user_id: uuid.UUID) -> List[Dict[str, str]]:
    """An endpoint to filter the shops based on certain query params
    
    Args:
        user_id (string): id of the logged in user
    """
    filters = ["newest", "oldest", "status"]
    filter = request.args.get("filter", None, str)
    page = request.args.get("page", 1, int)
    
    if filter not in filters or filter is None:
        return jsonify(
            {
                "message": "Bad Request",
                "error": "You need to pass in a filter"
            }
        ), 400
    try:
        if filter == "newest":
            shops = Shop.query.order_by(Shop.createdAt.desc()).paginate(page=page, per_page=10, error_out=False)
        elif filter == "status":
            # shops = Shop.query.filter_by(restricted="no", is_deleted="active").order_by(Shop.createdAt.desc()).paginate(page=page, per_page=10, error_out=False)
            shops = sort_by_top_sales(page=page, status=True)
            total_shops_count = total_shop_count(status=True)
        elif filter == "oldest":
            shops = Shop.query.order_by(Shop.createdAt.asc()).paginate(page=page, per_page=10, error_out=False)
        data = []
   
    except Exception as error:
        return jsonify({
            "message": "Bad Request",
            "error": f"{error} is not recognized"
        })

    def check_status(shop):
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
    # I know there's a better way to get number of pages but for the sake of the
    # sort_by_top_sales function which returns a list, I had to do it this way
    if isinstance(shops, list):
        total_shops = total_shops_count
        total_no_of_pages = total_shops / 10
        total_remainder = total_shops % 10
        if total_remainder > 0:
            total_no_of_pages += 1
    else:
        total_shops = Shop.query.count()
        total_no_of_pages = shops.pages
    banned_shops = Shop.query.filter(Shop.admin_status.in_(['suspended', 'blacklisted']), Shop.restricted == 'temporary').count()
    deleted_shops = Shop.query.filter_by(is_deleted="temporary").count()

    try:
        for shop in shops:
            total_products = Product.query.filter_by(shop_id=shop.id).count()
            merchant_name = f"{shop.user.first_name} {shop.user.last_name}"
            joined_date = shop.createdAt.strftime("%d-%m-%Y")
            shop_data = {
                "vendor_id": shop.id,
                "vendor_name": shop.name,
                "merchant_id": shop.merchant_id,
                "merchant_name": merchant_name,
                "merchant_email": shop.user.email,
                "merchant_location": shop.user.location,
                "merchant_country": shop.user.country,
                "vendor_profile_pic": vendor_profile_image(shop.merchant_id),
                "policy_confirmation": shop.policy_confirmation,
                "restricted": shop.restricted,
                "admin_status": shop.admin_status,
                "is_deleted": shop.is_deleted,
                "reviewed": shop.reviewed,
                "rating": shop.rating,
                "createdAt": shop.createdAt,
                "joined_date": joined_date,
                "updatedAt": shop.updatedAt,
                "vendor_status": check_status(shop),
                "total_products": total_products,
            }
            data.append(shop_data)
        return jsonify(
            {
                "message": "all shops information", 
                "data": data, 
                "total_shops": total_shops,
                "total_banned_shops": banned_shops, 
                "total_deleted_shops": deleted_shops,
                "total_pages": int(total_no_of_pages)
                }
        ), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e.__doc__)}), 500
    
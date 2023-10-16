from flask import Blueprint, jsonify, request
from super_admin_1 import db
from super_admin_1.models.alternative import Database
from super_admin_1.models.product import Product
from super_admin_1.models.product_category import Product_category
from super_admin_1.models.shop import Shop
from super_admin_1.logs.product_action_logger import (
    register_action_d,
    logger,
)
from utils import admin_required, image_gen, vendor_profile_image
from super_admin_1.notification.notification_helper import notify
from super_admin_1.products.product_schemas import IdSchema
from pydantic import ValidationError
from super_admin_1.logs.product_action_logger import register_action_d, logger
from utils import raise_validation_error
import json


product = Blueprint("product", __name__, url_prefix="/api/admin/product")

# WORKS #TESTED AND DOCUMENTED
@product.route("/all", methods=["GET"])
@admin_required(request=request)
def get_products(user_id):
    """get information related to a product

    Returns:
       dict: A JSON response with the appropriate status code and message.
           - If the products are returned successfully:
               - Status code: 200
               - Body:
                   - "message": "all products information"
                   - "data": []
                   - "total_products": 0
                   - "total_deleted_products": 0
                   - "total_sanctioned_products": 0
           - If an exception occurs during the get process:
               - Status code: 500
               - Body:
                   - "error": "Internal Server Error"
                   - "message": [error message]
    """
    product_shop_data = []

    def check_product_status(product):
        if product.admin_status == "suspended":
            return "Sanctioned"
        if (product.admin_status == "approved" or product.admin_status == "pending") and product.is_deleted == "active":
            return "Active"
        if product.is_deleted == "temporary":
            return "Deleted"

    products = Product.query.all()

    total_products = Product.query.count()
    sanctioned_products = Product.query.filter_by(
        admin_status='suspended', is_deleted='temporary').count()
    deleted_products = Product.query.filter_by(is_deleted="temporary").count()

    try:
        for product in products:
            shop = Shop.query.filter_by(id=product.shop_id).first()
            merchant_name = f"{shop.user.first_name} {shop.user.last_name}"
            data = {
                "product_image": image_gen(product.id),
                "admin_status": product.admin_status,
                "category_id": product.category_id,
                "user_id": product.user_id,
                "createdAt": product.createdAt,
                "currency": product.currency,
                "description": product.description,
                "discount_price": product.discount_price,
                "product_id": product.id,
                "is_deleted": product.is_deleted,
                "is_published": product.is_published,
                "product_name": product.name,
                "price": product.price,
                "quantity": product.quantity,
                "rating_id": product.rating_id,
                "shop_id": product.shop_id,
                "tax": product.tax,
                "updatedAt": product.updatedAt,
                "product_status": check_product_status(product),
                "shop_name": shop.name,
                "vendor_name": merchant_name,
                "category_name": product.product_category.name,
                "sub_category_name": product.product_category.product_sub_categories[0].name if product.product_category.product_sub_categories else None
            }
            product_shop_data.append(data)
        return jsonify({"message": "all products information", "data": product_shop_data, "total_products": total_products, "total_deleted_products": deleted_products, "total_sanctioned_products": sanctioned_products})
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


# to be reviewed #TESTED AND DOCUMENTED
@product.route("/<product_id>", methods=["GET"])
@admin_required(request=request)
def get_product(user_id, product_id):
    """get information related to a product

    Args:
        product_id (uuid): The unique identifier of the product.

     Returns:
        dict: A JSON response with the appropriate status code and message.
            - If the product is returned successfully:
                - Status code: 200
                - Body:
                    - "message": "the product information"
                    - "data": []
            - If the product with the given ID does not exist:
                - Status code: 404
                - Body:
                    - "error": "not found"
                    - "message": "invalid product id"
            - If an exception occurs during the get process:
                - Status code: 500
                - Body:
                    - "error": "Internal Server Error"
                    - "message": [error message]
    """
    try:
        product_id = IdSchema(id=product_id)
        product_id = product_id.id
        product = Product.query.filter_by(id=product_id).first()

        product_shop_data = []

        def check_product_status(product):
            if product.admin_status == "suspended":
                return "Sanctioned"
            if (product.admin_status == "approved" or product.admin_status == "pending") and product.is_deleted == "active":
                return "Active"
            if product.is_deleted == "temporary":
                return "Deleted"

        if not product:
            return jsonify({"error": "Not found", "message": "Product Not Found"}), 404

        shop = Shop.query.filter_by(id=product.shop_id).first()  #object of the shop
        merchant_name = f"{shop.user.first_name} {shop.user.last_name}"
        data = {
            "product_image": image_gen(product.id),
            "vendor_profile_pic":  vendor_profile_image(shop.merchant_id),    #come back to thisi
            "admin_status": product.admin_status,
            "category_id": product.category_id,
            "user_id": product.user_id,
            "createdAt": product.createdAt,
            "currency": product.currency,
            "description": product.description,
            "discount_price": product.discount_price,
            "product_id": product.id,
            "is_deleted": product.is_deleted,
            "is_published": product.is_published,
            "product_name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "rating_id": product.rating_id,
            "shop_id": product.shop_id,
            "tax": product.tax,
            "updatedAt": product.updatedAt,
            "product_status": check_product_status(product),
            "shop_name": shop.name,
            "vendor_name": merchant_name,
            "category_name": product.product_category.name,
            "sub_category_name": product.product_category.product_sub_categories[0].name if product.product_category.product_sub_categories else None
        }
        product_shop_data.append(data)

        return jsonify(
            {
                "message": "product successfull retrieved",
                "data": product_shop_data,
            }
        ), 200
    except ValidationError as e:
        raise_validation_error(e)
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@product.route("/sanction/<product_id>", methods=["PATCH"])
@admin_required(request=request)
def to_sanction_product(user_id, product_id):
    """sanctions a product by setting their
    is_deleted attribute  to "temporary"
    admin_status attribute to "blacklisted"
    Args:
        product_id (string)
    returns:
        JSON response with status code and message:
        -success(HTTP 200): product is sanctioned successfully
        -success(HTTP 200): if the product with provided not marked as sanctioned
        -failure(HTTP 404): if the product with provided id does not exist
        -failure(HTTP 500): if there is any server error
    """
    try:
        product_id = IdSchema(id=product_id)
        product_id = product_id.id
    except ValidationError as e:
        raise_validation_error(e)

    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return jsonify(
            {"error": "Product Not Found", "message": "Product does not exist"}
        ), 404

    if product.is_deleted == "temporary" or product.admin_status == "suspended":
        return jsonify(
            {
                "error": "Conflict",
                "message": "Product has already been sanctioned"
            }
        ), 409

    # Start a transaction
    db.session.begin_nested()

    # Update product attributes
    product.admin_status = "suspended"

    # Commit the transaction
    db.session.commit()

    # ========================Log and notify the owner of the sanctioning action====================
    try:
        register_action_d(user_id, "Product Sanction", product_id)
        notify(action="sanction", product_id=product_id)
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
    # ==============================================================================================

    return jsonify(
        {
            "data": product.format(),
            "message": "Product sanctioned successfully",
        }
    ), 200


# WORKS #TESTED AND DOCUMENTED
@product.route("/product_statistics", methods=["GET"])
@admin_required(request=request)
def get_product_statistics(user_id):
    """
    Returns statistics about the products, including the total number of all products, the total number of sanctioned
    products, and the total number of deleted products.

    :return: A JSON response containing product statistics.
    :rtype: dict
    """
    try:
        all_products = Product.query.count()
        sanctioned_products = Product.query.filter_by(
            admin_status="suspended", is_deleted="temporary"
        ).count()
        deleted_products = Product.query.filter_by(
            is_deleted="temporary").count()

        statistics = {
            "total_products": all_products,
            "total_sanctioned_products": sanctioned_products,
            "total_deleted_products": deleted_products,
        }

        return jsonify({"status": "Success", "product_statistics": statistics}), 200

    except Exception as exc:
        return jsonify(
            {
                "error": "Bad request",
                "message": "Something went wrong while retrieving product statistics: {exc}",
            }
        ), 400

# WORKS #TESTED AND DOCUMENTED
@product.route("/restore_product/<product_id>", methods=["PATCH"])
@admin_required(request=request)
def to_restore_product(user_id, product_id):
    """restores a temporarily deleted product by setting their is_deleted
        attribute from "temporary" to "active"
    Args:
        product_id (string)
    returns:
        JSON response with status code and message:
        -success(HTTP 200): product restored successfully

        -success(HTTP 200): if the product with provproduct_ided not marked as deleted
        -failure(HTTP 404): if the product with provproduct_ided product_id does not exist

        -success(HTTP 200): if the product with provided not marked as deleted
        -failure(HTTP 404): if the product with provided id does not exist

    """
    try:
        product_id = IdSchema(id=product_id)
        product_id = product_id.id
    except ValidationError as e:
        raise_validation_error(e)

    try:
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return jsonify(
                {
                    "error": "Product Not Found",
                    "message": " Product Already deleted",
                }
            ), 404

        if product.is_deleted == "temporary":
            product.is_deleted = "active"
            db.session.commit()


            # ========================Log and notify the owner of the restored action====================
            try:
                register_action_d(user_id, "Product Restored", product_id)
            except Exception as error:
                logger.error(f"{type(error).__name__}: {error}")
            # ==============================================================================================


            return jsonify(
                {
                    'message': 'product restored successfully',
                    "data": product.format()
                }
            ), 201
        else:
            return jsonify(
                {
                    "message": "product is not marked as deleted",
                    "error": "conflict"
                }
            ), 409
    except Exception as exc:
        logger.error(f"{type(exc).__name__}: {exc}")
        return jsonify(
            {
                "error": "Bad request",
                "message": "Something went wrong while performing this Action",
            }
        ), 400


# WORKS #TESTED AND DOCUMENTED
@product.route("delete_product/<product_id>", methods=["PATCH"])
@admin_required(request=request)
def temporary_delete(user_id, product_id):
    """
    Deletes a product temporarily by updating the 'is_deleted' field of the product in the database to 'temporary'.
    Logs the action in the product_logs table.

    Args:
        product_id (str): The product_id of the product to be temporarily deleted.

    Returns:
        dict: A JSON response with the appropriate status code and message.
            - If the product is successfully temporarily deleted:
                - Status code: 204
                - Body:
                    - "message": "Product temporarily deleted"
                    - "data": null
            - If the product with the given product_id does not exist:
                - Status code: 404
                - Body:
                    - "error": "Not Found"
                    - "message": "Product not found"
            - If an exception occurs during the logging process:
                - Status code: 500
                - Body:
                    - "error": "Internal Server Error"
                    - "message": [error message]
    """
    select_query = """
                        SELECT * FROM public.product
                        WHERE id=%s;"""

    delete_query = """UPDATE product
                        SET is_deleted = 'temporary'
                        WHERE id = %s;"""
    update_query = """
            UPDATE "product"
            SET "is_deleted" = 'temporary', 
            WHERE "id" = %s
            RETURNING *;  -- Return the updated row
        """

    try:
        product_id = IdSchema(id=product_id)
        product_id = product_id.id
    except ValidationError as e:
        raise_validation_error(e)
    try:
        with Database() as db:
            db.execute(select_query, (product_id,))
            selected_product = db.fetchone()
            print(f"selected product: {selected_product}")
            if not selected_product:
                return jsonify({"error": "Not Found", "message": "Product not found"}), 404
            if selected_product[11] == "temporary":
                return jsonify(
                    {
                        "error": "Conflict",
                        "message": "Action already carried out on this Product",
                    }
                ), 409

            db.execute(delete_query, (product_id,))
            print(f"header: {request.headers.get('Content-Type')}")
            if request.headers.get("Content-Type") == "application/json":
                # Catch the error for non-existent JSON payload and dependent logger
                try:
                    data = request.json()
                    reason = data.get("reason")
                    register_action_d(user_id, f"Temporary Deletion for Reason: {reason}", product_id)
                except Exception as error:
                    logger.error(f"{type(error).__name__}: {error}")

            try:
                register_action_d(user_id, f"Temporary Deletion", product_id)
            except Exception as log_error:
                logger.error(f"{type(log_error).__name__}: {log_error}")

        return jsonify(
            {
                "message": "Product temporarily deleted",
                "data": None,
            }
        ), 204
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500


# WORKS #TESTED AND DOCUMENTED
@product.route("approve_product/<product_id>", methods=["PATCH"])
@admin_required(request=request)
def approve_product(user_id, product_id):
    """
    Approves a product  by updating the 'admin_status' field of the product in the database to 'approved'.
    Logs the action in the product_logs table.

    Args:
        product_id (uuid): The product_id of the product to be temporarily deleted.

    Returns:
            - If succed a status code of 204, and NO content.
            - If the product with the given product_id does not exist:
                - Status code: 404
                - Body:
                    - "error": "Not Found"
                    - "message": "Product not found"
            - If an exception occurs during the logging process:
                - Status code: 500
                - Body:
                    - "error": "Internal Server Error"
                    - "message": [error message]
    """
    select_query = """
                        SELECT * FROM public.product
                        WHERE id=%s;"""

    approve_query = """UPDATE product
                        SET admin_status = 'approved'
                        WHERE id = %s;"""

    try:
        product_id = IdSchema(id=product_id)
        product_id = product_id.id
    except ValidationError as e:
        raise_validation_error(e)
    try:
        with Database() as db:
            db.execute(select_query, (product_id,))
            selectedproduct = db.fetchone()
            if not selectedproduct:
                return jsonify({"error": "Not Found", "message": "Product not found"}), 404
            if selectedproduct[10] == "approved":
                return jsonify(
                    {
                        "error": "Conflict",
                        "message": "Action already carried out on this Product",
                    }
                ), 409
            

            db.execute(approve_query, (product_id,))
            db.execute(select_query, (product_id,))
            selected_product = db.fetchone()
        if selected_product:
            data = {
                "id": selected_product[0],
                "shop_id": selected_product[1],
                "name": selected_product[2],
                "description": selected_product[3],
                "quantity": selected_product[4],
                "category_id": selected_product[5],
                "user_id": selected_product[6],
                "price": float(selected_product[7]),
                "discount_price": float(selected_product[8]),
                "tax": float(selected_product[9]),
                "admin_status": selected_product[10],
                "is_deleted": selected_product[11],
                "rating_id": selected_product[12],
                "is published": selected_product[13],
                "currency": selected_product[14],
                "created_at": str(selected_product[15]),
                "updated_at": str(selected_product[16]),
            }

            try:
                register_action_d(user_id, "Product Approval", product_id)
                notify(action="unsanction", product_id=product_id)

            except Exception as log_error:
                logger.error(f"{type(log_error).__name__}: {log_error}")
        return jsonify(
            {
                "message": "Product approved successfully",
                  "data": data
            }
        ), 201

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


# WORKS #TESTED AND DOCUMENTED
@product.route("delete_product/<product_id>", methods=["DELETE"])
@admin_required(request=request)
def permanent_delete(user_id, product_id):
    """
    Deletes a product permanently from the database.

    Args:
        user_id (uuid): The ID of the user performing the deletion.
        product_id (uuid): The UUID of the product to be deleted.

    Returns:
         response indicating the success status code of 204 with NO Content or failure of the deletion.
        If the `product_id` is not a valid UUID, return a JSON response with a "Bad Request" error and a message indicating the unsupported data type.
        If the product is not found in the database, return a JSON response with a "Not Found" error and a message indicating that the product was not found.
        If there is an error while executing the DELETE query or logging the action, return a JSON response with a "Server Error" error and a message indicating the error.
        If the deletion is successful, return a JSON response with a "Product permanently deleted" message and a null data field.
    """
    select_query = """
                        SELECT id FROM public.product
                        WHERE id =%s;"""
    delete_query = """DELETE FROM public.product 
                                WHERE id = %s; """

    try:
        product_id = IdSchema(id=product_id)
        product_id = product_id.id
    except ValidationError as e:
        raise_validation_error(e)
    try:            
        with Database() as db:
            db.execute(select_query, (product_id,))
            deleteproduct = db.fetchone()
            if not deleteproduct:
                return jsonify({"error": "Not Found", "message": "Product not found"}), 404
            db.execute(delete_query, (product_id,))
            try:
                register_action_d(user_id, "Permanent Product Deletion", product_id)
                notify(action="deletion", product_id=product_id)

            except Exception as log_error:
                logger.error(f"{type(log_error).__name__}: {log_error}")
        return jsonify({
            "message": "Product Permanently Deleted from the Database",
            "data": None
        }), 204
    
    except Exception as e:
        return jsonify(
            {
                "error": "Internal Server Error",
                "message": "we are currently experiencing a downtime with this feature"
            }
        ), 500




# Define a route to get all temporarily deleted products

# WORKS #TESTED AND DOCUMENTED
@product.route("/temporarily_deleted_products", methods=["GET"], strict_slashes=False)
@admin_required(request=request)
def get_temporarily_deleted_products(user_id):
    """
    Retrieve temporarily deleted products.
    This endpoint allows super admin users to retrieve a list of products that have been temporarily deleted.
    Returns:
        JSON response with status and message:
        - Success (HTTP 200): A list of temporarily deleted products and their details.
        - Success (HTTP 200): A message indicating that no products have been temporarily deleted.
        - Error (HTTP 500): If an error occurs during the retrieving process.
    Permissions:
        - Only accessible to super admin users.
    Note:
        - The list includes the details of products that have been temporarily deleted.
        - If no products have been temporarily deleted, a success message is returned.
    """
    try:
        # Query the database for all temporarily_deleted_products
        temporarily_deleted_products = Product.query.filter_by(
            is_deleted="temporary"
        ).all()

        # Calculate the total count of temporarily deleted products
        total_count = len(temporarily_deleted_products)

        # Check if no products have been temporarily deleted
        if not temporarily_deleted_products:
            return jsonify(
                {
                    "message": "No products have been temporarily deleted, Yet!",
                    "data": total_count,
                }
            ), 200

        # Create a list with Product details
        products_list = [product.format()
                         for product in temporarily_deleted_products]

        # Return the list with all attributes of the temporarily_deleted_products
        return jsonify(
            {
                "message": "All temporarily deleted products retrieved successfully",
                "data": {
                    "temporarily_deleted_products": products_list,
                    "count": total_count,
                }
            }
        ), 200
    except Exception as e:
        # Handle any exceptions that may occur during the retrieving process
        return jsonify({"status": "Error", "message": str(e)})

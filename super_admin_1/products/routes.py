from flask import Blueprint, jsonify
from super_admin_1 import db
from super_admin_1.models.alternative import Database
from super_admin_1.models.product import Product
from super_admin_1.logs.product_action_logger import (
    register_action_d,
    logger,
)

from super_admin_1.products.product_schemas import IdSchema
from pydantic import ValidationError
from super_admin_1.logs.product_action_logger import register_action_d, logger
from utils import raise_validation_error


product = Blueprint("product", __name__, url_prefix="/api/product")


# WORKS
@product.route("/all", methods=["GET"])
# @admin_required(request=request)
def get_products(user_id):
    """get information related to a product

    Returns:
       dict: A JSON response with the appropriate status code and message.
           - If the products are returned successfully:
               - Status code: 200
               - Body:
                   - "message": "all products request successful"
                   - "data": []
           - If an exception occurs during the get process:
               - Status code: 500
               - Body:
                   - "error": "Internal Server Error"
                   - "message": [error message]
    """
    try:
        products = Product.query.all()
        return (
            jsonify(
                {
                    "message": "all products request successful",
                    "data": [product.format() for product in products],
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


# WORKS
@product.route("/<product_id>", methods=["GET"])
# @admin_required(request=request)
def get_product(product_id):
    """get information related to a product

    Args:
        product_id (uuid): The unique identifier of the product.

     Returns:
        dict: A JSON response with the appropriate status code and message.
            - If the product is returned successfully:
                - Status code: 200
                - Body:
                    - "message": "the product request successful"
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
        if not product:
            return jsonify({"error": "Not found", "message": "Product Not Found"}), 404

        return (
            jsonify(
                {
                    "message": "the product request successful",
                    "data": [product.format()],
                }
            ),
            200,
        )
    except ValidationError as e:
        raise_validation_error(e)
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500



# NOT WORKING ORM ISSUE
@product.route("/sanction/<product_id>", methods=["PATCH"])
# @admin_required(request=request)
def to_sanction_product(product_id):
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
        return (
            jsonify(
                {"error": "Product Not Found", "message": "Product does not exist"}
            ),
            404,
        )


    if product.is_deleted == "temporary" and product.admin_status == "suspended":
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
    product.is_deleted = "temporary"

    # Commit the transaction
    db.session.commit()

    # ========================Log and notify the owner of the sanctioning action====================
    try:
        register_action_d(user_id, "Product Sanction", product_id)
        notify(action="sanction", product_id=product_id)
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
    # ==============================================================================================

    return (
        jsonify(
            {
                "data": product.format(),
                "message": "Product sanctioned successfully",
            }
        ),
        200,
    )


# WORKS
@product.route("/product_statistics", methods=["GET"])
# @admin_required(request=request)
def get_product_statistics():
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
        deleted_products = Product.query.filter_by(is_deleted="temporary").count()

        statistics = {
            "total_products": all_products,
            "total_sanctioned_products": sanctioned_products,
            "total_deleted_products": deleted_products,
        }

        return jsonify({"status": "Success", "product_statistics": statistics}), 200

    except Exception as exc:
        return (
            jsonify(
                {
                    "error": "Bad request",
                    "message": "Something went wrong while retrieving product statistics: {exc}",
                }
            ),
            400,
        )


# Not fully working
@product.route("/restore_product/<product_id>", methods=["PATCH"])
# @admin_required(request=request)
def to_restore_product(product_id):
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
        print(product)
        if not product:
            return (
                jsonify(
                    {
                        "error": "Product Not Found",
                        "message": " Product Already deleted",
                    }
                ),
                404,
            )

        if product.is_deleted == "temporary":
            if product.admin_status == "suspended" or product.admin_status == "approved":
                product.admin_status = "approved"
                product.is_deleted = "active"
                db.session.commit()
                register_action_d(
                    user_id,
                    "Restore Temporary Deletion",
                    product_id,
                )


                return jsonify(
                    {
                        'message': 'product restored successfully',
                        "data": product.format()
                        }
                        ), 201

        else:
            return jsonify({"message": "product is not marked as deleted"}), 200
    except Exception as exc:
        logger.error(f"{type(exc).__name__}: {exc}")
        return (
            jsonify(
                {
                    "error": "Bad request",
                    "message": "Something went wrong while performing this Action",
                }
            ),
            400,
        )


# WORKS
@product.route("delete_product/<product_id>", methods=["PATCH"])
# @admin_required(request=request)
def temporary_delete(product_id):
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
            if len(selected_product) == 0:
                return (
                    jsonify({"error": "Not Found", "message": "Product not found"}),
                    404,
                )
            if selected_product[10] == "temporary":
                return (
                    jsonify(
                        {
                            "error": "Conflict",
                            "message": "Action already carried out on this Product",
                        }
                    ),
                    409,
                )

            db.execute(delete_query, (product_id,))

            # data = request.get_json()
            # reason = data.get("reason")

            # if not reason:
            #     return jsonify({"error": "Supply a reason for deleting this product."}), 400

            try:
                register_action_d(user_id, "Temporary Deletion", product_id)
            except Exception as log_error:
                logger.error(f"{type(log_error).__name__}: {log_error}")

        return (
            jsonify(
                {
                    "message": "Product temporarily deleted",
                    # "reason": reason,
                    "data": None,
                }
            ),
            204,
        )

    except Exception as e:
        print("here")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


# WORKS
@product.route("delete_product/<product_id>", methods=["DELETE"])
# @admin_required(request=request)
def permanent_delete(product_id):
    """
    Deletes a product permanently from the database.

    Args:
        user_id (int): The ID of the user performing the deletion.
        product_id (str): The UUID of the product to be deleted.

    Returns:
        A JSON response indicating the success or failure of the deletion.
        If the `product_id` is not a valid UUID, return a JSON response with a "Bad Request" error and a message indicating the unsupported data type.
        If the product is not found in the database, return a JSON response with a "Not Found" error and a message indicating that the product was not found.
        If there is an error while executing the DELETE query or logging the action, return a JSON response with a "Server Error" error and a message indicating the error.
        If the deletion is successful, return a JSON response with a "Product permanently deleted" message and a null data field.
    """

    try:
        product_id = IdSchema(id=product_id)
        product_id = product_id.id
    except ValidationError as e:
        raise_validation_error(e)

    try:
        with Database() as db:
            check_query = "SELECT * FROM product WHERE id = %s;"
            db.execute(check_query, (product_id,))
            product = db.fetchone()

            if len(product) == 0:
                return (
                    jsonify({"error": "Not Found", "message": "Product not found"}),
                    404,
                )

            delete_query = """DELETE FROM product WHERE id = %s;"""
            db.execute(delete_query, (product_id,))

            # log and notify of deletion
            try:
                register_action_d(user_id, "Permanent Deletion", product_id)
                notify(action="deletion", product_id=product_id)
            except Exception as error:
                logger.error(f"{type(error).__name__}: {error}")

        return jsonify({"message": "Product permanently deleted", "data": None}), 204
    except Exception as exc:
        return jsonify({"error": "Server Error", "message": str(exc)}), 500


# Define a route to get all temporarily deleted products


# WORKS
@product.route("/temporarily_deleted_products", methods=["GET"], strict_slashes=False)
# @admin_required(request=request)
def get_temporarily_deleted_products():
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
            return (
                jsonify(
                    {
                        "message": "No products have been temporarily deleted, Yet!",
                        "data": total_count,
                    }
                ),
                200,
            )

        # Create a list with Product details
        products_list = [product.format() for product in temporarily_deleted_products]

        # Return the list with all attributes of the temporarily_deleted_products
        return (
            jsonify(
                {
                    "message": "All temporarily deleted products retrieved successfully",
                    "data": {
                        "temporarily_deleted_products": products_list,
                        "count": total_count,
                    },
                }
            ),
            200,
        )
    except Exception as e:
        # Handle any exceptions that may occur during the retrieving process
        return jsonify({"status": "Error", "message": str(e)})


# Define a route to get details of a temporarily deleted product based on ID
@product.route(
    "/temporarily_deleted_product/<string:product_id>",
    methods=["GET"],
    strict_slashes=False,
)
# @admin_required(request=request)
def get_temporarily_deleted_product(user_id, product_id):
    """
    Retrieve details of a temporarily deleted product based on its ID.

    Args:
        product_id (int): The unique identifier of the product to retrieve.

    Returns:
        JSON response with status and message:
        - Success (HTTP 200): Details of the temporarily deleted product.
        - Error (HTTP 404): If the product with the provided ID is not found.
        - Error (HTTP 500): If an error occurs during the retrieval process.

    Permissions:
        - Only accessible to super admin users.

    Note:
        - This endpoint allows super admin users to retrieve the details of a temporarily deleted product based on its ID.
    """
    try:
        # Validate that product_id is a valid UUID in hexadecimal form
        product_id = IdSchema(id=product_id)
        product_id = product_id.id

        # Query the database for the product with the provided product_id that is temporarily deleted
        temporarily_deleted_product = Product.query.filter_by(
            id=product_id, is_deleted="temporary"
        ).first()

        # If the product with the provided ID doesn't exist or is not temporarily deleted, return a 404 error
        if not temporarily_deleted_product:
            return (
                jsonify(
                    {
                        "status": "Error",
                        "message": "Temporarily deleted product not found.",
                    }
                ),
                404,
            )

        # Return the details of the temporarily deleted product
        product_details = temporarily_deleted_product.format()

        return (
            jsonify(
                {
                    "status": "Success",
                    "message": "Temporarily deleted product details retrieved successfully",
                    "temporarily_deleted_product": product_details,
                }
            ),
            200,
        )
    except ValidationError as e:
        raise_validation_error(e)
    except SQLAlchemyError as e:
        # Handle any exceptions that may occur during the retrieval process
        db.session.rollback()
        return jsonify({"status": "Error", "message": str(e)}), 500


# @product.route("/remove_sanction/<product_id>", methods=["PATCH"])
# # @admin_required(request=request)
# def to_remove_sanction_product(user_id, product_id):
#     """remove sanctions on a product by setting their
#     is_deleted attribute from "temporary" to "active"
#     admin_status attribute from "suspended" to "approved"
#     Args:
#         product_id (string)
#     returns:
#         JSON response with status code and message:
#         -success(HTTP 200): product sanctioned is removed successfully
#         -success(HTTP 200): if the product with provided not marked as sanctioned
#         -failure(HTTP 404): if the product with provided id does not exist
#     """
#     try:
#         product_id = IdSchema(id=product_id)
#         product_id = product_id.id
#     except ValidationError as e:
#         raise_validation_error(e)

#     try:
#         product = Product.query.filter_by(id=product_id).first()
#         if not product:
#             return jsonify(
#                     {
#                         "error": "Conflict",
#                         "message": " Product Already deleted",
#                     }
#                 ), 409

#         if product.is_deleted == "temporary" and product.admin_status == "suspended":
#             try:
#                 # Start a transaction
#                 db.session.begin_nested()

#                 # Update product attributes to remove the sanction
#                 product.admin_status = "approved"
#                 product.is_deleted = "active"

#                 # Commit the transaction
#                 db.session.commit()

#                 # Log the removal of the sanction
#                 try:
#                     register_action_d(
#                         user_id,
#                         "Product Sanction removal",
#                         product_id,
#                     )
#                 except Exception as log_error:
#                     return jsonify({"error": "Logging Error", "message": str(log_error)}), 500

#                 return jsonify(
#                         {
#                             "data": product.format(),
#                             "message": "Sanction removed successfully",
#                         }
#                     ), 200

#             except Exception as e:
#                 db.session.rollback()
#                 return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
#         else:
#             return jsonify({"message": "product is not marked as sanctioned"}), 200
#     except Exception as exc:
#         return jsonify(
#                 {
#                     "error": "Bad request {}".format(exc),
#                     "message": "Something went wrong while performing this Action",
#                 }
#             ), 400


# @product.route("/sanctioned_products/", methods=["GET"])
# # @admin_required(request=request)
# def get_sanctioned_products(user_id):
#     """
#     Retrieves the details of sanctioned products.

#     :return: A JSON response containing the details of the sanctioned product.
#     :rtype: dict
#     """
#     try:
#         products = Product.query.all()
#         if not products:
#             return jsonify(
#                     {
#                         "error": "Product Not Found",
#                         "message": " Product Already deleted",
#                     }
#             ), 404
#         santioned_product_list = []
#         for product in products:
#             if (
#                 product.admin_status == "suspended"
#                 and product.is_deleted == "temporary"
#             ):
#                 santioned_product_list.append(product.format())

#         return jsonify(
#                 {
#                     "status": "Success",
#                     "message": "Sanctioned products returned successfully",
#                     "data": santioned_product_list
#                 }
#         ), 200

#     except Exception as exc:
#         return jsonify(
#                 {
#                     "error": "Bad request {}".format(exc),
#                     "message": "Something went wrong while performing this Action",
#                 }
#         ), 400

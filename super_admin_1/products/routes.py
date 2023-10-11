from flask import Blueprint, jsonify, send_file
from super_admin_1 import db
from super_admin_1.models.alternative import Database
from utils import super_admin_required
from super_admin_1.models.product import Product
from super_admin_1.products.event_logger import generate_log_file_d, register_action_d
import os


product = Blueprint("product", __name__, url_prefix="/api/product")


@product.route("restore_product/<product_id>", methods=["PATCH"])
@super_admin_required
def to_restore_product(product_id):
    """restores a temporarily deleted product by setting their is_deleted
        attribute from "temporary" to "active"
    Args:
        product_id (string)
    returns:
        JSON response with status code and message:
        -success(HTTP 200): product restored successfully
        -success(HTTP 200): if the product with provided not marked as deleted
        -failure(HTTP 404): if the product with provided id does not exist

    """

    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return jsonify({"message": "Invalid product"}), 404

    if product.is_deleted == "temporary":
        product.is_deleted = "active"
        db.session.commit()
        return jsonify({"message": "product restored successfully"}), 200
    else:
        return jsonify({"message": "product is not marked as deleted"}), 200


@product.route("delete_product/<id>", methods=["PATCH"])
@super_admin_required
def temporary_delete(id):
    """
    Deletes a product temporarily by updating the 'is_deleted' field of the product in the database to 'temporary'.
    Logs the action in the product_logs table.

    Args:
        id (str): The ID of the product to be temporarily deleted.

    Returns:
        dict: A JSON response with the appropriate status code and message.
            - If the product is successfully temporarily deleted:
                - Status code: 204
                - Body:
                    - "message": "Product temporarily deleted"
                    - "data": null
            - If the product with the given ID does not exist:
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
    try:
        # SQL query to mark the product as 'temporary' deleted
        delete_query = """UPDATE public.product
                          SET is_deleted = 'temporary'
                          WHERE id = %s;"""

        with Database() as db:
            db.execute(delete_query, (id,))
            affected_rows = db.rowcount

            if affected_rows == 0:
                return (
                    jsonify({"error": "Not Found", "message": "Product not found"}),
                    404,
                )

        try:
            register_action_d(
                "683f379e-9302-4445-9d35-efda5c9a8133", "Temporary Deletion", id
            )
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

        return jsonify({"message": "Product temporarily deleted", "data": None}), 204

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


# Define a route to get all temporarily deleted products
@product.route("/temporarily_deleted_products", methods=["GET"], strict_slashes=False)
@super_admin_required
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

        # Check if no products have been temporarily deleted
        if not temporarily_deleted_products:
            return (
                jsonify(
                    {
                        "status": "Success",
                        "message": "No products have been temporarily deleted, Yet!",
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
                    "status": "Success",
                    "message": "All temporarily deleted products retrieved successfully",
                    "temporarily_deleted_products": products_list,
                }
            ),
            200,
        )

    except Exception as e:
        # Handle any exceptions that may occur during the retrieving process
        return jsonify({"status": "Error", "message": str(e)})


@product.route("delete_product/<id>", methods=["DELETE"])
@super_admin_required
def permanent_delete(id):
    # Ensure the id is a string
    if not isinstance(id, str):
        return jsonify({"error": "Bad Request", "message": "Invalid ID Data-Type"})

    # No authentication at the moment to check if user is logged in or have rights to delete.
    try:
        # Check if the product exists and delete it permanently
        with Database() as db:
            # First, check if the product exists
            check_query = "SELECT * FROM product WHERE id = %s;"
            db.execute(check_query, (str(id),))
            product = db.fetchone()

            if not product:
                return jsonify({"error": "Not Found", "message": "Product not found"})

            # Delete the product permanently
            delete_query = """DELETE FROM product WHERE id = %s;"""
            db.execute(delete_query, (str(id),))

            # Check if the product was deleted
            if db.rowcount == 0:
                return jsonify(
                    {"error": "Not Found", "message": "No product was deleted"}
                )

            # Log the action
            try:
                register_action_d(
                    "550e8400-e29b-41d4-a716-446655440000", "Permanent Deletion", id
                )
            except Exception as log_error:
                return (
                    jsonify({"error": "Logging Error", "message": str(log_error)}),
                    500,
                )

        return jsonify({"message": "Product permanently deleted", "data": "None"}), 204
    except Exception as exc:
        return jsonify({"error": "Server Error", "message": str(exc)}), 500


@product.route("/download/log")
@super_admin_required
def log():
    """Download product logs"""
    filename = generate_log_file_d()
    if filename is False:
        return {"message": "No log entry exists"}, 204
    path = os.path.abspath(filename)
    return send_file(path)

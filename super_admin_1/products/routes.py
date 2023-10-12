from flask import Blueprint, jsonify, request
from super_admin_1 import db
from super_admin_1.models.alternative import Database
from super_admin_1.models.product import Product
from super_admin_1.logs.product_action_logger import register_action_d, logger
import uuid
from utils import super_admin_required
from super_admin_1.notification.notification_helper import notify, notify_test


product = Blueprint("product", __name__, url_prefix="/api/product")


@product.route('/all', methods=['GET'])
@super_admin_required
def get_products():
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
        return jsonify(
            {
                "message": "all products request successful",
                "data": [product.format() for product in products]
            }
        ),  200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@product.route('/<product_id>', methods=['GET'])
@super_admin_required
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

        if not product:
            return jsonify({"error": "not found", "message": "invalid product id"}), 404

        return jsonify(
            {
                "message": "the product request successful",
                "data": [product.format()]
            }
        ),  200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


product.route('restore_product/<product_id>', methods=['PATCH'])
# @super_admin_required


def to_restore_product(product_id):
    """restores a temporarily deleted product by setting their is_deleted
        attribute from "temporary" to "active"
    Args:
        product_id (uuid)
    returns:
        JSON response with status code and message:
        -success(HTTP 200): product restored successfully
        -success(HTTP 200): if the product with provproduct_ided not marked as deleted
        -failure(HTTP 404): if the product with provproduct_ided product_id does not exist
         """
    try:
        uuid.UUID(product_id)
    except ValueError as exc:
        jsonify(
            {
                "error": "Bad Request",
                "message": f"Type: {type(product_id)} product_id  not supported"
            }
        ), 400
    try:
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return jsonify(
                {
                    "error":  "Product Not Found",
                    'message': ' Product Already deleted'
                }
            ), 404

        if product.is_deleted == 'temporary':
            product.is_deleted = "active"
            db.session.commit()

            print(product)
            return jsonify(
                {
                    'message': 'product restored successfully',
                    "data": "data"
                }
            ), 201
        else:
            return jsonify({'message': 'product is not marked as deleted'}), 200
    except Exception as exc:
        print(str(exc))
        return jsonify(
            {
                "error": "Bad request",
                "message": "Something went wrong while performing this Action",
            }
        ), 400


# DONE!
@product.route("delete_product/<product_id>", methods=["PATCH"])
@super_admin_required
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
        uuid.UUID(product_id)
    except ValueError as E:
        return jsonify(
            {"error": "Bad Request",
             "message": f"Type: {type(product_id)} product_id Data-Type not supported"
             }
        ), 400
    try:
        with Database() as db:
            db.execute(select_query, (product_id,))
            selected_product = db.fetchone()
            if len(selected_product) == 0:
                return jsonify({"error": "Not Found", "message": "Product not found"}), 404
            if selected_product[10] == "temporary":
                return jsonify(
                    {
                        "error": "Conflict",
                        "message": "Action already carried out on this Product"
                    }
                ), 409

            db.execute(delete_query, (product_id,))

            data = request.get_json()
            reason = data.get("reason")

            if not reason:
                return jsonify({"error": "Supply a reason for deleting this product."}), 400

            try:
                register_action_d(user_id, "Temporary Deletion", product_id)
                # notify()
                # notify_test("Delete")
            except Exception as log_error:
                logger.error(f"{type(log_error).__name__}: {log_error}")

        return jsonify({"message": "Product temporarily deleted", "reason": reason, "data": None}), 204

    except Exception as e:
        print("here")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@product.route("delete_product/<product_id>", methods=["DELETE"])
@super_admin_required
def permanent_delete(user_id, product_id):
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
        uuid.UUID(product_id)
    except ValueError as E:
        return jsonify({"error": "Bad Request", "message": f"Type: {type(product_id)} product_id Data-Type not supported"}), 400

    try:
        with Database() as db:
            check_query = "SELECT * FROM product WHERE id = %s;"
            db.execute(check_query, (product_id,))
            product = db.fetchone()

            if len(product) == 0:
                return jsonify({"error": "Not Found", "message": "Product not found"}), 404

            delete_query = """DELETE FROM product WHERE id = %s;"""
            db.execute(delete_query, (product_id,))

            try:
                register_action_d(user_id, "Permanent Deletion", product_id)
            except Exception as log_error:
                logger.error(f"{type(log_error).__name__}: {log_error}")

        return jsonify(
            {
                "message": "Product permanently deleted",
                "data": None
            }
        ), 204
    except Exception as exc:
        return jsonify({"error": "Server Error", "message": str(exc)}), 500

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
        products_list = [product.format()
                         for product in temporarily_deleted_products]

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
    

    



@product.route("/sanctioned", methods=["GET"])
# @super_admin_required
def sanctioned_products():
  """
  Get all sanctioned products from the database.
  
  Args:
    None
  
  Returns:
    A JSON response containing a message and a list of dictionary objects representing the sanctioned products.
    If no products are found, the message will indicate that and the object will be set to None.
  """
  data = []
  # get all the product object, filter by is_delete = temporay and rue and admin_status = "suspended"
  query = Product.query.filter(
    Product.admin_status == "suspended",
  )
    
  # if the query is empty
  if not query.all():
    return jsonify({
        "message": "No products found",
        "object": None
    }), 200
  # populate the object to a list of dictionary object
  for obj in query:
    data.append(obj.format())

  return jsonify({
    "message": "All sanctioned products",
    "object": data
    }), 200

#======= HELPER FUNCTION===============
@product.route("/all", methods=["GET"])
# @super_admin_required
def all_products():
  """ Get all product in database as a list of dictionary object"""
  data = []
  # get all products data
  query = Product.query.all()
  # if the query is empty
  if not query:
    return jsonify({
      "message": "No products found",
      "object": None
    }), 200
  # populate the object to a list of dictionary object
  for obj in query:
    data.append(obj.format())
  return jsonify({
    "message": "All products",
    "object": data
    }), 200
   # =================HELPER FUNCTION END=============

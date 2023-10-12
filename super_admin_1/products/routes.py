from flask import Blueprint, jsonify, send_file
from super_admin_1 import db
from super_admin_1.models.alternative import Database
from utils import super_admin_required
from super_admin_1.models.product import Product
from super_admin_1.products.event_logger import generate_log_file_d, register_action_d
import os, uuid
from utils import super_admin_required


product = Blueprint('product', __name__, url_prefix='/api/product')



@product.route('restore_product/<product_id>', methods=['PATCH'])
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


#DONE!
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
            if selected_product[10]  == "temporary":
                return jsonify(
                    {
                        "error": "Conflict",
                        "message": "Action already carried out on this Product"
                    }
                ), 409            

            db.execute(delete_query, (product_id,))
            try:
                register_action_d(user_id,"Temporary Deletion", product_id)
            except Exception as e:
                return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

        return jsonify(
            {
                "message": "Product temporarily deleted", 
                "data": None
            }
        ),  204

    except Exception as e:
        print("here")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    



    #DONE
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
                return jsonify({"error": "Logging Error", "message": str(log_error)}), 500

        return jsonify(
            {
                "message": "Product permanently deleted",
                "data": None
            }
        ), 204
    except Exception as exc:
        return jsonify({"error": "Server Error", "message": str(exc)}), 500


    
@product.route("/download/log")
@super_admin_required
def log():
    """Download product logs"""
    filename = generate_log_file_d()
    if filename is False:
        return jsonify(
            {
                "error": "File Not Found",
            "message": "No log entry exists"
        }
        ), 404
    path = os.path.abspath(filename)
    return send_file(path)

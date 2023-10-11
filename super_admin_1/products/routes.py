from flask import Blueprint, jsonify, send_file
from super_admin_1 import db
from super_admin_1.models.alternative import Database
from utils import super_admin_required
from super_admin_1.models.product import Product
from super_admin_1.products.event_logger import generate_log_file_d, register_action_d
import os
from utils import super_admin_required


product = Blueprint('product', __name__, url_prefix='/api/product')


# ===============implement an endpoint to fetch a products and fetch a shop and all the product associated with the shop in the databse===========================
@product.route("/product/<product_id>", methods=["GET"])
def get_product(product_id):
    select_query = """
    SELECT * FROM public.product
     WHERE product_id=%s;""" 
    with Database as db:
        try:
            if not isinstance(product_id, str):
                return jsonify(
                    {
                        "error": "Bad request",
                        "message": "Invalproduct_id product_id Data-Type ",
                    }
                    ), 400
            db.execute(select_query, (product_id,))
            result = db.fetchone()
            if not result:
                return jsonify({
                    "error": "Not found",
                    "message": "The specified product was not found"
                }), 404
            print(result)
            #  TODO: SERIALIZE THE DATA AND RENDER IT =========
            return jsonify(
                {
                    "message": "successful",
                    "data": "something",
                }
            ), 200
        except Exception as exc:
            print(str(exc))
            return jsonify({
                "error": "Bad request",
                "message": "something went wrong while processing your request",
            })

    return "products"




@product.route('restore_product/<product_product_id>', methods=['PATCH'])
@super_admin_required
def to_restore_product(product_product_id):
    """restores a temporarily deleted product by setting their is_deleted
        attribute from "temporary" to "active"
    Args:
        product_product_id (string)
    returns:
        JSON response with status code and message:
        -success(HTTP 200): product restored successfully
        -success(HTTP 200): if the product with provproduct_ided not marked as deleted
        -failure(HTTP 404): if the product with provproduct_ided product_id does not exist
         """

    product = Product.query.filter_by(product_id=product_product_id).first()
    if not product:
        return jsonify({'message': 'Invalproduct_id product'}), 404

    if product.is_deleted == 'temporary':
        product.is_deleted = "active"
        db.session.commit()
        return jsonify({'message': 'product restored successfully'}), 200
    else:
        return jsonify({'message': 'product is not marked as deleted'}), 200

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
    try:
        # SQL query to mark the product as 'temporary' deleted
        select_query = """
                            SELECT * FROM product
                            WHERE product_id=%s;""" 
        delete_query = """UPDATE product
                          SET is_deleted = 'temporary'
                          WHERE product_id = %s;"""

        with Database() as db:
            print("db connection")
            if not isinstance(product_id, str):
                return jsonify({"error": "Bad Request", "message": f"Type: {type(product_id)} product_id Data-Type not supported"})
            db.execute(select_query, (product_id,))
            selected_product = db.fetchone()
            print(selected_product)
            if selected_product == 0:
                return jsonify({"error": "Not Found", "message": "Product not found"}), 404
            

            db.execute(delete_query, (str(product_id),))


        try:
            print("adeyemo")
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
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
@product.route("delete_product/<product_id>", methods=["DELETE"])
@super_admin_required
def permanent_delete(product_id):
    # Ensure the product_id is a string
    if not isinstance(product_id, str):
        return jsonify({"error": "Bad Request", "message": "Invalproduct_id product_id Data-Type"})

    # No authentication at the moment to check if user is logged in or have rights to delete.
    try:
        # Check if the product exists and delete it permanently
        with Database() as db:
            # First, check if the product exists
            check_query = "SELECT * FROM product WHERE product_id = %s;"
            db.execute(check_query, (str(product_id),))
            product = db.fetchone()

            if not product:
                return jsonify({"error": "Not Found", "message": "Product not found"})

            # Delete the product permanently
            delete_query = """DELETE FROM product WHERE product_id = %s;"""
            db.execute(delete_query, (str(product_id),))

            # Check if the product was deleted
            if db.rowcount == 0:
                return jsonify({"error": "Not Found", "message": "No product was deleted"})

            # Log the action
            try:
                register_action_d("550e8400-e29b-41d4-a716-446655440000", "Permanent Deletion", product_id)
            except Exception as log_error:
                return jsonify({"error": "Logging Error", "message": str(log_error)}), 500

        return jsonify({"message": "Product permanently deleted", "data": "None"}), 204
    except Exception as exc:
        return jsonify({"error": "Server Error", "message": str(exc)}), 500
    
@product.route("/download/log")
@super_admin_required
def log():
    """Download product logs"""
    filename = generate_log_file_d()
    if filename is False:
        return {
            "message": "No log entry exists"
        }, 204
    path = os.path.abspath(filename)
    return send_file(path)

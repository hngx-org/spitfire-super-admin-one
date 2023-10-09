from flask import Blueprint, jsonify, send_file
from super_admin_1.models.alternative import Database
from super_admin_1.products.event_logger import generate_log_file_d, register_action_d
import os
from flask_login import login_required

product_delete = Blueprint("product_delete", __name__, url_prefix="/api/product")


@product_delete.route("/<id>", methods=["PATCH"])
@login_required
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
                return jsonify({"error": "Not Found", "message": "Product not found"}), 404

        try:
            register_action_d("683f379e-9302-4445-9d35-efda5c9a8133","Temporary Deletion", id)
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



@product_delete.route("/download/log")
@login_required
def log():
    """Download product logs"""
    filename = generate_log_file_d()
    path = os.path.abspath(filename)
    return send_file(path)

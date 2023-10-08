from flask import Blueprint, jsonify, request, send_file
from super_admin_1.models.alternative import Database
from super_admin_1.products.event_logger import generate_log_file_d, register_action_d
import os

product_delete = Blueprint("product_delete", __name__, url_prefix="/api/product")


@product_delete.route("/<id>", methods=["PATCH"])
def temporary_delete(id):
    # THIS IS WHERE I VALIDATE IF THE USER IS AUTHORIZED TO ACCESS THIS ROUTE I.E THE 403 STATUS CODE
    if not isinstance(id, str):
        return jsonify({"error": "Bad Request", "message": "invalid ID Data-Type"})
    try:
        delete_query = """UPDATE public.product
                                    SET is_deleted = 'temporary'
                                    WHERE id = %s;"""

        with Database() as db:
            db.execute(delete_query, id)
            product = db.fetchone()
        if not product:
            return jsonify({"error": "Not Found", "message": "Not Found"}), 404
        print(product)
        try:
            register_action_d(
                "550e8400-e29b-41d4-a716-446655440000", "Temporary Deletion", id
            )
        except:
            pass

        return (
            jsonify({"message": "Product Temporarily deleted", "data": "None"}),
            204,
        )  # 204 doesn't return a response, so no content to be displayed
    except Exception as exc:
        print(exc)
        return (
            jsonify(
                {
                    "message": "Something went wrong while Deleting this Product, Try again later",
                    "Error": "Bad Request",
                }
            ),
            500,
        )


@product_delete.route("/download/log")
def log():
    """Download product logs"""
    filename = generate_log_file_d()
    path = os.path.abspath(filename)
    return send_file(path)

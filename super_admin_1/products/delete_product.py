from flask import Blueprint, jsonify, request
from super_admin_1.models.alternative import Database

product_delete = Blueprint("product_delete", __name__, url_prefix="/api/product")

@product_delete.route("/<id>", methods=["PATCH"])
def temporary_delete(id):
    # THIS IS WHERE I VALIDATE IF THE USER IS AUTHORIZED TO ACCESS THIS ROUTE I.E THE 403 STATUS CODE
    if not isinstance(id, str):
        return jsonify({
            "error": "Bad Request",
            "message": "invalid ID Data-Type"
        })
    try:
        delete_query = """UPDATE public.product
                                    SET is_deleted = 'temporary'
                                    WHERE id = %s;"""

        with Database() as db:
            db.execute(delete_query, id)
            print(db)
        return jsonify({
            "message": "Product Temporarily deleted",
            "data": "None"
        }), 204  
    except Exception as exc:
        print(exc)
        return jsonify({
            "message": "Something went wrong while Deleting this Product, Try again later",
            "Error": "Bad Request",
        })


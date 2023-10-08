#!/usr/bin/env python3
"""API Temlate for the Product-driven Operation"""

from flask import Blueprint, jsonify, request, abort
from super_admin_1.models.product import Product
from super_admin_1 import db

restore_product = Blueprint('restore_product', __name__,
                            url_prefix='/api/restore_product')


@restore_product.route('/<product_id>', methods=['PATCH'])
def to_restore_product(product_id):
    """restores a temporarily deleted product by setting their is_deleted
        attribute from "temporary" to "active"
    Args:
        product_id (string)
    returns:
        JSON response with status code and message:
        -success(HTTP 200): product restored successfully
        -success(HTTP 200): if the product with provided not marked as deleted
         """
    # data = request.get_json()
    # if not request.is_json:
    #     return jsonify({'message': 'JSON data required'}), 400
    #     # abort(400, 'JSON data required')
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return jsonify({'message': 'Invalid product'}), 404
        # abort(404, 'Invalid product')
    # change the object attribute from temporary to active
    if product.is_deleted == 'temporary':
        product.is_deleted = "active"
        db.session.commit()
        return jsonify({'message': 'product restored successfully'}), 200
    else:
        return jsonify({'message': 'product is not marked as deleted'}), 200



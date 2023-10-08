#!/usr/bin/env python3
"""API Temlate for the Product-driven Operation"""

from flask import Blueprint, jsonify, request, abort
from super_admin_1.models.product import Product
from super_admin_1 import db

restore_product = Blueprint('restore_product', __name__,
                            url_prefix='/api/restore_product')
delete_product = Blueprint('delete_product', __name__,
                            url_prefix='/api/delete_product') #Testing by Samuel Ogboye
create_product = Blueprint('create_product', __name__,
                           url_prefix='/api/create_product')

# -----------Samuel Ogboye Restoring Temporarily Deleted Products ------------


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


# -----------Samuel Ogboye to delete Products temporarily for testing purpose ------------
@delete_product.route('/<product_id>', methods=['PATCH'])
def ttemp_delete_product(product_id):
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
    if product.is_deleted == 'active':
        product.is_deleted = "temporary"
        db.session.commit()
        return jsonify({'message': 'product deleted temporarily successfully'}), 200
    else:
        return jsonify({'message': 'product is already deleted temporarily'}), 200

# -----------Samuel Ogboye to create Products for testing purpose ------------
@create_product.route('/', methods=['POST'])
def create_new_product():
    """Create a new product."""
    data = request.get_json()
    if not request.is_json:
        return jsonify({'message': 'JSON data required'}), 400
        # abort(400, 'JSON data required')

    # Extract data from the request
    name = data.get('name')
    description = data.get('description')
    quantity = data.get('quantity')
    price = data.get('price')
    discount_price = data.get('discount_price')
    tax = data.get('tax')
    admin_status = data.get('admin_status')
    is_deleted = data.get('is_deleted')
    is_published = data.get('is_published')
    currency = data.get('currency')

    # Validate data as needed

    # Create a new product object
    new_product = Product(name=name, description=description, quantity=quantity, price=price, discount_price=discount_price, tax=tax, admin_status=admin_status, is_deleted=is_deleted, is_published=is_published, currency=currency)

    # Add the product to the database
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product created successfully', 'product_id': new_product.id}), 201

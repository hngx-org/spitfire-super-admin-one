from flask import Blueprint, jsonify 
from super_admin_1 import db
from utils import super_admin_required
from super_admin_1.models.product import Product


product = Blueprint('product', __name__, url_prefix='/api/product')

@product.route('restore_product/<product_id>', methods=['PATCH'])
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
        return jsonify({'message': 'Invalid product'}), 404

    if product.is_deleted == 'temporary':
        product.is_deleted = "active"
        db.session.commit()
        return jsonify({'message': 'product restored successfully'}), 200
    else:
        return jsonify({'message': 'product is not marked as deleted'}), 200


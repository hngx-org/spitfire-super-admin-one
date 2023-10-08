from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from super_admin_1 import db
from super_admin_1.models.shop import Shop

shop_bp = Blueprint('shop', __name__, url_prefix='/api/shop')

@shop_bp.route('/unban_vendor/<string:vendor_id>', methods=['PUT'])
def unban_vendor(vendor_id):
    try:
        # Search db for passed vendor id
        vendor = Shop.query.filter_by(merchant_id=vendor_id).first()
        # If vendor id doesn't exist
        if not vendor:
            return jsonify(
                {
                    "status": "Error",
                    "message": "Vendor not found."
                }
            ), 404

        vendor.restricted = 'no'  # Unban the vendor
        vendor.admin_status = 'approved'  # Update the vendor's status
        db.session.commit() # Commit changes to the database

        return jsonify(
            {
                "status": "Success",
                "message": "Vendor unbanned successfully."
            }
        ), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(
            {
                "message": "An error occurred.",
                "error": str(e)
            }
        ), 500

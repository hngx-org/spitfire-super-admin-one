from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from super_admin_1 import db
from super_admin_1.models.shop import Shop

# Create a Flask Blueprint for shop-related operations
shop_bp = Blueprint('shop', __name__, url_prefix='/api/shop')

# Define a route to unban a vendor
@shop_bp.route('/unban_vendor/<string:vendor_id>', methods=['PUT'])
def unban_vendor(vendor_id):
    """
    Unban a vendor by setting their 'restricted' and 'admin_status' fields.

    Args:
        vendor_id (string): The unique identifier of the vendor to unban.

    Returns:
        JSON response with status and message:
        - Success (HTTP 200): Vendor unbanned successfully.
        - Error (HTTP 404): If the vendor with the provided ID is not found.
        - Error (HTTP 500): If an error occurs during the database operation.

    Note:
    - This endpoint is used to unban a vendor by updating their 'restricted' and 'admin_status' fields.
    - The 'restricted' field is set to 'no' to indicate that the vendor is no longer restricted.
    - The 'admin_status' field is set to 'approved' to indicate that the vendor's status has been updated.
    - Proper authentication and authorization checks should be added to secure this endpoint.
    """
    try:
        # Search the database for the vendor with the provided vendor_id
        vendor = Shop.query.filter_by(merchant_id=vendor_id).first()
        # If the vendor with the provided ID doesn't exist, return a 404 error
        if not vendor:
            return jsonify(
                {
                    "status": "Error",
                    "message": "Vendor not found."
                }
            ), 404

        # Unban the vendor by setting 'restricted' to 'no' and updating 'admin_status' to 'approved'
        vendor.restricted = 'no'
        vendor.admin_status = 'approved'

        # Commit the changes to the database
        db.session.commit()

        # Return a success message
        return jsonify(
            {
                "status": "Success",
                "message": "Vendor unbanned successfully."
            }
        ), 200
    except SQLAlchemyError as e:
        # If an error occurs during the database operation, roll back the transaction and return a 500 error
        db.session.rollback()
        return jsonify(
            {
                "message": "An error occurred.",
                "error": str(e)
            }
        ), 500

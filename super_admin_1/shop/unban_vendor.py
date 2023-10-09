from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from super_admin_1 import db
from super_admin_1.models.shop import Shop
from flask_login import login_required
import uuid

# Create a Flask Blueprint for shop-related operations
shop_blueprint = Blueprint("shop_blueprint", __name__, url_prefix="/api/shop")


# Define a route to unban a vendor
@shop_blueprint.route("/unban_vendor/<string:vendor_id>", methods=["PUT"])
@login_required
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
        try:
            uuid.UUID(vendor_id, version=4)
        except ValueError:
            # If it's a value error, then the string
            # is not a valid hex code for a UUID.
            return jsonify({"status": "Error", "message": "Invalid UUID format."}), 400

        # Search the database for the vendor with the provided vendor_id
        vendor = Shop.query.filter_by(id=vendor_id).first()
        # If the vendor with the provided ID doesn't exist, return a 404 error
        if not vendor:
            return (
                jsonify({"status": "Error", "message": "Vendor not found."}),
                404,
            )  # Not found

        # Check if the shop associated with the vendor is active
        if vendor.is_deleted != "active":
            return (
                jsonify(
                    {
                        "status": "Error",
                        "message": "Vendor's shop is not active. Cannot unban.",
                    }
                ),
                400,
            )  # Bad request

        # Check if the vendor is already unbanned
        if vendor.restricted == "no":
            return (
                jsonify({"status": "Error", "message": "Vendor is already unbanned."}),
                400,
            )

        # Unban the vendor by setting 'restricted' to 'no' and
        # updating 'admin_status' to 'approved'
        vendor.restricted = "no"
        vendor.admin_status = "approved"

        # Commit the changes to the database
        db.session.commit()

        # Construct vendor details for the response
        vendor_details = {
            "id": vendor.id,
            "merchant_id": vendor.merchant_id,
            "name": vendor.name,
            "policy_confirmation": vendor.policy_confirmation,
            "restricted": vendor.restricted,
            "admin_status": vendor.admin_status,
            "is_deleted": vendor.is_deleted,
            "reviewed": vendor.reviewed,
            "rating": float(vendor.rating),
            "created_at": str(vendor.created_at),
            "updated_at": str(vendor.updated_at),
        }

        # Return a success message
        return (
            jsonify(
                {
                    "status": "Success",
                    "message": "Vendor unbanned successfully.",
                    "vendor_details": vendor_details,
                }
            ),
            200,
        )
    except SQLAlchemyError as e:
        # If an error occurs during the database operation, roll back the transaction
        db.session.rollback()
        return jsonify({"status": "Error.", "message": str(e)}), 500

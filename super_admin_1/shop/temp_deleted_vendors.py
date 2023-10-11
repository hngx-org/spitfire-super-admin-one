from flask import Blueprint, jsonify
from super_admin_1 import db
from super_admin_1.models.shop import Shop
from utils import super_admin_required
import uuid

deleted_vendors = Blueprint("deleted_vendors", __name__, url_prefix="/api/shop")


# Define a route to get all temporarily deleted vendors
@deleted_vendors.route("/temporarily_deleted_vendors", methods=["GET"])
@super_admin_required
def get_temporarily_deleted_vendors():
    """
    Retrieve temporarily deleted vendors.

    This endpoint allows super admin users to retrieve a list of vendors who have been temporarily deleted.

    Returns:
        JSON response with status and message:
        - Success (HTTP 200): A list of temporarily deleted vendors and their details.
        - Success (HTTP 200): A message indicating that no vendors have been temporarily deleted.
        - Error (HTTP 500): If an error occurs during the retrieving process.

    Permissions:
        - Only accessible to super admin users.

    Note:
        - The list includes the details of vendors who have been temporarily deleted.
        - If no vendors have been temporarily deleted, a success message is returned.
    """
    try:
        # Query the database for all temporarily_deleted_vendors
        temporarily_deleted_vendors = Shop.query.filter_by(is_deleted="temporary").all()

        # Check if no vendors have been temporarily deleted
        if not temporarily_deleted_vendors:
            return (
                jsonify(
                    {
                        "status": "Success",
                        "message": "No vendors have been temporarily deleted",
                    }
                ),
                200,
            )

        # Create a list with vendors details
        vendors_list = [vendor.format() for vendor in temporarily_deleted_vendors]

        # Return the list with all attributes of the temporarily_deleted_vendors
        return (
            jsonify(
                {
                    "status": "Success",
                    "message": "All temporarily deleted vendors retrieved successfully",
                    "temporarily_deleted_vendors": vendors_list,
                }
            ),
            200,
        )

    except Exception as e:
        # Handle any exceptions that may occur during the retrieving process
        return jsonify({"status": "Error", "message": str(e)})


# ... (previous code)

# =====================HELPER FUNCTIONS=========================================
# Commented out the helper functions and routes as requested
# Define a route to get all vendors, including all their details
# @deleted_vendors.route("/all_vendors", methods=["GET"])
# def get_all_vendors():
#     try:
#         # Retrieve all vendors from the database
#         vendors = Shop.query.all()

#         # Check if there are vendors to return
#         if not vendors:
#             return jsonify({"message": "No vendors found."}), 200

#         # Prepare the list of vendors with all their details
#         vendor_list = [vendor.format() for vendor in vendors]

#         return jsonify({"vendors": vendor_list}), 200
#     except Exception as e:
#         return jsonify({"status": "Error", "message": str(e)})

# Commented out the route to temporarily delete a vendor
# Define a route to temporarily delete a vendor
# @deleted_vendors.route("/delete_vendor/<string:vendor_id>", methods=["DELETE"])
# def temporarily_delete_vendor(vendor_id):
#     try:
#         # Check if the vendor_id is a valid UUID (assuming vendor IDs are UUIDs)
#         if not is_valid_uuid(vendor_id):
#             return jsonify({"error": "Invalid vendor ID format."}), 400

#         # Find the vendor by ID and set their status to "temporary" deleted
#         vendor = Shop.query.filter_by(id=vendor_id).first()
#         if vendor:
#             vendor.is_deleted = "temporary"
#             db.session.commit()
#             return jsonify(
#                 {
#                     "status": "Success",
#                     "message": "Vendor temporarily deleted successfully."}), 200
#         else:
#             return jsonify({"error": "Vendor not found."}), 404
#     except Exception as e:
#         return jsonify({"status": "Error", "message": str(e)})

# Commented out the helper function to check if a string is a valid UUID
# Helper function to check if a string is a valid UUID
# def is_valid_uuid(uuid_string):
#     try:
#         uuid.UUID(uuid_string, version=4)
#         return True
#     except ValueError:
#         return False

# ... (remaining code)

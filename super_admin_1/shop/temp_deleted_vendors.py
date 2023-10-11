from Flask import Blueprint, jsonify
from super_admin_1 import db
from super_admin_1.models.shop import Shop
from utils import super_admin_required

deleted_vendors = Blueprint("deleted_vendors", __name__, url_prefix="api/shop")


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

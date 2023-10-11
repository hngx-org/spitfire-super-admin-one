from Flask import Blueprint, jsonify
from super_admin_1 import db
from super_admin_1.models.shop import Shop
from utils import super_admin_required

deleted_vendors = Blueprint("deleted_vendors", __name__, url_prefix="api/shop")


# Define a route to get all temporarily deleted vendors
@deleted_vendors.route("/temporarily_deleted_vendors", methods=["GET"])
@super_admin_required
def get_temporarily_deleted_vendors():
    """ """
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

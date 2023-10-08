from flask import Blueprint, jsonify
from super_admin_1.models.alternative import Database

shop = Blueprint("shop", __name__, url_prefix="/api/shop")


# TEST
@shop.route("/endpoint", methods=["GET"])
def shop_endpoint():
    """
    Handle GET requests to the shop endpoint.

    Returns:
        jsonify: A JSON response indicating the success of the request.
    """
    response_data = {"message": "This is the shop endpoint under /api/shop/endpoint"}
    return jsonify(response_data), 200


@shop.route("/ban_vendor/<uuid:user_id>", methods=["PUT"])
def ban_vendor(user_id):
    """
    Handle PUT requests to ban a vendor by updating their shop data.

    Args:
        user_id (uuid): The unique identifier of the vendor to be banned.

    Returns:
        jsonify: A JSON response containing the status of the vendor banning operation.
    """
    try:
        update_query = """
            UPDATE "shop"
            SET "restricted" = 'temporary', 
                "admin_status" = 'suspended'
            WHERE "merchant_id" = %s
            RETURNING *;  -- Return the updated row
        """
        with Database() as cursor:
            cursor.execute(update_query, (user_id,))
            updated_vendor = cursor.fetchone()

        if updated_vendor:
            vendor_details = {
                "id": updated_vendor[0],
                "merchant_id": updated_vendor[1],
                "name": updated_vendor[2],
                "policy_confirmation": updated_vendor[3],
                "restricted": updated_vendor[4],
                "admin_status": updated_vendor[5],
                "is_deleted": updated_vendor[6],
                "reviewed": updated_vendor[7],
                "rating": float(updated_vendor[8]),
                "created_at": str(updated_vendor[9]),
                "updated_at": str(updated_vendor[10]),
            }
            return (
                jsonify(
                    {
                        "message": "Vendor account banned temporarily.",
                        "vendor_details": vendor_details,
                    }
                ),
                200,
            )
        else:
            return jsonify({"error": "Vendor not found."}), 404

    except Exception as e:
        print(str(e))
        return jsonify({"error": "Internal Server Error"}), 500


@shop.route("/banned_vendors", methods=["GET"])
def get_banned_vendors():
    try:
        # Perform a database query to retrieve all banned vendors
        query = """
            SELECT * FROM "shop"
            WHERE "restricted" = 'temporary' AND "admin_status" = 'suspended'
        """

        with Database() as cursor:
            cursor.execute(query)
            banned_vendors = cursor.fetchall()

        # Prepare the response data
        banned_vendors_list = []
        for vendor in banned_vendors:
            vendor_details = {
                "id": vendor[0],
                "merchant_id": vendor[1],
                "name": vendor[2],
                "policy_confirmation": vendor[3],
                "restricted": vendor[4],
                "admin_status": vendor[5],
                "is_deleted": vendor[6],
                "reviewed": vendor[7],
                "rating": float(vendor[8]),
                "created_at": str(vendor[9]),
                "updated_at": str(vendor[10]),
            }
            banned_vendors_list.append(vendor_details)

        # Return the list of banned vendors in the response
        return jsonify({"banned_vendors": banned_vendors_list}), 200

    except Exception as e:
        print(str(e))
        return jsonify({"error": "Internal Server Error"}), 500

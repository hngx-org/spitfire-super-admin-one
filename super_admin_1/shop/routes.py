from flask import Blueprint, jsonify, abort, send_file, request
import uuid, os
from super_admin_1.models.alternative import Database
from super_admin_1 import db
from super_admin_1.models.shop import Shop
from super_admin_1.models.shop_logs import ShopsLogs
from super_admin_1.shop.shoplog_helpers import ShopLogs
from sqlalchemy.exc import SQLAlchemyError
from utils import super_admin_required
# from super_admin_1.models.product import Product

shop = Blueprint("shop", __name__, url_prefix="/api/shop")

# TEST
@shop.route("/endpoint", methods=["GET"])
@super_admin_required
def shop_endpoint():
    """
    Handle GET requests to the shop endpoint.

    Returns:
        jsonify: A JSON response indicating the success of the request.
    """
    response_data = {"message": "This is the shop endpoint under /api/shop/endpoint"}
    return jsonify(response_data), 200


@shop.route("/ban_vendor/<uuid:vendor_id>", methods=["PUT"])
@super_admin_required
def ban_vendor(vendor_id):
    """
    Handle PUT requests to ban a vendor by updating their shop data.

    Args:
        vendor_id (uuid): The unique identifier of the vendor to be banned.

    Returns:
        jsonify: A JSON response containing the status of the vendor banning operation.
    """
    try:
        # Check if the vendor is already banned
        check_query = """
            SELECT "restricted" FROM "shop"
            WHERE "id" = %s
        """
        with Database() as cursor:
            cursor.execute(check_query, (str(vendor_id),))
            current_state = cursor.fetchone()

        if current_state and current_state[0] == 'temporary':
            return jsonify({"error": "Vendor is already banned."}), 400

        # Proceed with banning the vendor
        update_query = """
            UPDATE "shop"
            SET "restricted" = 'temporary', 
                "admin_status" = 'suspended'
            WHERE "id" = %s
            RETURNING *;  -- Return the updated row
        """
        with Database() as cursor:
            cursor.execute(update_query, (str(vendor_id),))
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
@super_admin_required
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
        return jsonify(
            {   
                "message": "Banned vendors retrieved successfully.",
                "banned_vendors": banned_vendors_list
            }
        ), 200

    except Exception as e:
        print(str(e))
        return jsonify({"error": "Internal Server Error"}), 500
    
# Define a route to unban a vendor
@shop.route("/unban_vendor/<string:vendor_id>", methods=["PUT"])
@super_admin_required
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

@shop.route("restore_shop/<shop_id>", methods=["PATCH"])
@super_admin_required
def restore_shop(shop_id):
    """restores a deleted shop by setting their "temporary" to "active" fields
    Args:
        shop_id (string)
    returns:
        JSON response with status code and message:
        -success(HTTP 200):shop restored successfully
        -success(HTTP 200): if the shop with provided not marked as deleted
    """
    # data = request.get_json()
    # if not request.is_json:
    # abort(400), "JSON data required"
    shop = Shop.query.filter_by(id=shop_id).first()
    if not shop:
        abort(404), "Invalid shop"
    # change the object attribute from temporary to active
    if shop.is_deleted == "temporary":
        shop.is_deleted = "active"
        try:
            db.session.commit()

            """
            The following logs the action in the shop_log db
            """
            get_user_id = shop.user.id
            action = ShopLogs(
                shop_id=shop_id,
                user_id=get_user_id
            )
            action.log_shop_deleted(delete_type="active")

            return jsonify({"message": "shop restored successfully"}), 200
        except Exception as e:
            db.session.rollback()
            abort(500, f"Failed to restore shop: {str(e)}")
    else:
        return jsonify({"message": "shop is not marked as deleted"}), 200
    
@shop.route('delete_shop/<shop_id>', methods=['PATCH'], strict_slashes=False)
@super_admin_required
def delete_shop(shop_id):
    """Delete a shop and cascade temporary delete action to products"""
    # verify if shop exists
    shop = Shop.query.filter_by(id=shop_id).first()
    if not shop:
        return jsonify({'forbidden': 'Shop not found'}), 404
    # check if shop is temporary
    if shop.is_deleted == 'temporary':
        return jsonify({'message': 'Shop already deleted'}), 400
    
    # # Cascade the temporary delete action to associated products
    # products = Product.query.filter_by(shop_id=shop_id).all()
    # for product in products:
    #     product.is_deleted = 'temporary'
    #     db.session.add(product)

    # Delete the shop temporarily
    shop.is_deleted = 'temporary'
    db.session.commit()

    """
    The following logs the action in the shop_log db
    """
    get_user_id = shop.user.id
    action = ShopLogs(
        shop_id=shop_id,
        user_id=get_user_id
    )
    action.log_shop_deleted(delete_type="temporary")
    # return jsonify({'message': 'Shop and associated products temporarily deleted'}), 200


# delete shop object permanently out of the DB
@shop.route('delete_shop/<shop_id>', methods=['DELETE'])
@super_admin_required
def perm_del(shop_id):
    """ Delete a shop"""
    shop = Shop.query.filter_by(id=shop_id).first()
    if not shop:
        abort(404)
    db.session.delete(shop)
    db.session.commit()
    return jsonify({'message': 'Shop deleted aggresively'}), 200



logs = Blueprint("logs", __name__, url_prefix="/api/logs")

@logs.route("/shops", defaults={"shop_id": None})
@logs.route("/shops/<int:shop_id>")
@super_admin_required
def get_all_shop_logs(shop_id):
    """Get all shop logs"""
    if not shop_id:
        return (
            jsonify(
                {
                    "message": "success",
                    "logs": [
                        log.format() if log else [] for log in ShopsLogs.query.all()
                    ],
                }
            ),
            200,
        )

    return (
        jsonify(
            {
                "message": "success",
                "logs": [
                    log.format() if log else []
                    for log in ShopsLogs.query.filter_by(shop_id=shop_id).all()
                ],
            }
        ),
        200,
    )


@logs.route("/shops/download", defaults={"shop_id": None})
@logs.route("/shops/<int:shop_id>/download")
@super_admin_required
def download_shop_logs(shop_id):
    """Download all shop logs"""
    logs = []
    if not shop_id:
        logs = [log.format() if log else [] for log in ShopsLogs.query.all()]
    else:
        logs = [
            log.format() if log else []
            for log in ShopsLogs.query.filter_by(shop_id=shop_id).all()
        ]
    # Create a temporary file to store the strings
    temp_file_path = f"{os.path.abspath('.')}/temp_file.txt"
    with open(temp_file_path, "w") as temp_file:
        temp_file.write("\n".join(logs))

    response = send_file(
        temp_file_path, as_attachment=True, download_name="shoplogs.txt"
    )
    os.remove(temp_file_path)

    return response

@logs.route("/shop/actions", methods=["GET"])
@super_admin_required
def shop_actions():
    data = ShopsLogs.query.all()
    return jsonify([action.format_json() for action in data]), 200
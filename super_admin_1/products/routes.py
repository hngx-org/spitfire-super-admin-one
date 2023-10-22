from flask import Blueprint, jsonify, request
from super_admin_1 import db
from super_admin_1.models.alternative import Database
from super_admin_1.models.product import Product
from super_admin_1.models.shop import Shop
from super_admin_1.logs.product_action_logger import (
    register_action_d,
    logger,
)
from utils import admin_required, image_gen, vendor_profile_image
from super_admin_1.notification.notification_helper import notify
from super_admin_1.products.product_schemas import IdSchema
from uuid import UUID


product = Blueprint("product", __name__, url_prefix="/api/v1/admin/products")

@product.route("/all", methods=["GET"])
@admin_required(request=request)
def get_products(user_id : UUID) -> dict:
    """
    Get products and their information.

    Args:
        user_id (UUID): The ID of the user.

    Returns:
        dict: A dictionary containing the following information:
            - "message" (str): The message indicating the success of the operation.
            - "data" (list): A list of dictionaries containing the product information.
            - "total_products" (int): The total number of products.
            - "total_deleted_products" (int): The total number of deleted products.
            - "total_sanctioned_products" (int): The total number of sanctioned products.
            - "total_pages" (int): The total number of pages.

    Raises:
        Exception: If there is an internal server error.

    Examples:
        # Example 1: Get all products
        get_products(user_id)

        # Example 2: Get products with search and status filters
        get_products(user_id, search="example", status="sanctioned")
    """
    product_shop_data = []

    def check_product_status(product):
        if product.admin_status in ["suspended", "blacklisted"]:
            return "Sanctioned"
        elif (
            product.admin_status in ["approved"]
            and product.is_deleted == "active"
        ):
            return "Active"
        elif product.is_deleted == "temporary":
            return "Deleted"

    page = request.args.get('page',1 , int)
    search = request.args.get('search',None)
    status = request.args.get('status',None)
    # FOR ALL THE PRODUCTS AND THEIR COUNTS
    products = Product.query.order_by(Product.createdAt.desc()).paginate(page=page, per_page=10, error_out=False)
    total_products = products.total
    total_no_of_pages = products.pages
    sanctioned_products = Product.query.filter(Product.admin_status.in_(['suspended', 'blacklisted'])).count()
    deleted_products = Product.query.filter_by(is_deleted="temporary").count()
    if search and status:
        if status == "sanctioned":
        # FOR ALL THE SANCTIONED PRODUCTS  AND THEIR COUNTS
            products = Product.query.filter(
                Product.admin_status.in_(['suspended', 'blacklisted']),
                Product.name.ilike(f'%{search}%')
                ).order_by(
                Product.createdAt.desc()).paginate(page=page, per_page=10, error_out=False) 
            total_products = products.total
            total_no_of_pages = products.pages
        if status == "deleted":
        # FOR ALL THE DELETED PRODUCTS  AND THEIR COUNTS
            products = Product.query.filter(
                Product.is_deleted=="temporary", 
                Product.admin_status.in_(["pending", "approved", "reviewed"]),
                Product.name.ilike(f'%{search}%')
                ).order_by(
                Product.createdAt.desc()).paginate(page=page, per_page=10, error_out=False) 
            total_products = products.total
            total_no_of_pages = products.pages
    if search and not status:
        # FOR ALL THE RESULTS OF A SEARCH AND THEIR COUNTS
        products = Product.query.filter(Product.name.ilike(f'%{search}%')).order_by(Product.createdAt.desc()).paginate(page=page, per_page=10, error_out=False) 
        total_products = products.total
        total_no_of_pages = products.pages
    if status and not search:
        if status == "sanctioned":
        # FOR ALL THE SANCTIONED PRODUCTS  AND THEIR COUNTS
            products = Product.query.filter(Product.admin_status.in_(['suspended', 'blacklisted'])).order_by(Product.createdAt.desc()).paginate(page=page, per_page=10, error_out=False) 
            total_products = products.total
            total_no_of_pages = products.pages
        if status == "deleted":
        # FOR ALL THE DELETED PRODUCTS  AND THEIR COUNTS
            products = Product.query.filter(Product.is_deleted=="temporary", Product.admin_status.in_(["pending", "approved", "reviewed"])).order_by(Product.createdAt.desc()).paginate(page=page, per_page=10, error_out=False) 
            total_products = products.total
            total_no_of_pages = products.pages



    try:
        for product in products:
            shop = Shop.query.filter_by(id=product.shop_id).first()
            merchant_name = f"{shop.user.first_name} {shop.user.last_name}"
            data = {
                "product_image": image_gen(product.id),
                "admin_status": product.admin_status,
                "category_id": product.category_id,
                "user_id": product.user_id,
                "createdAt": product.createdAt,
                "currency": product.currency,
                "description": product.description,
                "discount_price": product.discount_price,
                "product_id": product.id,
                "is_deleted": product.is_deleted,
                "is_published": product.is_published,
                "product_name": product.name,
                "price": product.price,
                "quantity": product.quantity,
                "rating_id": product.rating_id,
                "shop_id": product.shop_id,
                "tax": product.tax,
                "updatedAt": product.updatedAt,
                "product_status": check_product_status(product),
                "shop_name": shop.name,
                "vendor_name": merchant_name,
                "category_name": product.product_category.name,
                "sub_category_name": product.product_category.product_sub_categories[0].name if product.product_category.product_sub_categories else ""
            }
            product_shop_data.append(data)
        return jsonify(
            {
                "message": "all products information", 
                "data": product_shop_data, 
                "total_products": total_products, 
                "total_deleted_products": deleted_products, 
                "total_sanctioned_products": sanctioned_products,
                "total_pages": int(total_no_of_pages)
                }
                ), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@product.route("/pending/all", methods=["GET"])
@admin_required(request=request)
def get_pending_products(user_id : UUID) -> dict:
    """
    Get pending products and their information.

    Args:
        user_id (UUID): The ID of the user.

    Returns:
        dict: A dictionary containing the following information:
            - "message" (str): The message indicating the success of the operation.
            - "data" (list): A list of dictionaries containing the pending product information.
            - "total_pending_products" (int): The total number of pending products.
            - "total_pages" (int): The total number of pages.

    Raises:
        Exception: If there is an internal server error.

    Examples:
        # Example 1: Get all pending products
        get_pending_products(user_id)

        # Example 2: Get pending products with search filter
        get_pending_products(user_id, search="example")
    """

    product_shop_data = []

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    #Query pending products with pagination and is_deleted filter
    products = Product.query.filter(
        Product.admin_status == 'pending',
        Product.is_deleted == 'active',  # Filter for products that are not deleted
        Product.name.ilike(f'%{search}%')) \
        .order_by(Product.createdAt.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    total_pending_products = products.total
    total_no_of_pages = products.pages



    try:
        for product in products.items:
            # Retrieve shop information for the product
            shop = Shop.query.filter_by(id=product.shop_id).first()
            merchant_name = f"{shop.user.first_name} {shop.user.last_name}"

            data = {
                "product_image": image_gen(product.id),
                "admin_status": product.admin_status,
                "category_id": product.category_id,
                "user_id": product.user_id,
                "createdAt": product.createdAt,
                "currency": product.currency,
                "description": product.description,
                "discount_price": product.discount_price,
                "product_id": product.id,
                "is_deleted": product.is_deleted,
                "is_published": product.is_published,
                "product_name": product.name,
                "price": product.price,
                "quantity": product.quantity,
                "rating_id": product.rating_id,
                "shop_id": product.shop_id,
                "tax": product.tax,
                "updatedAt": product.updatedAt,
                "shop_name": shop.name,
                "vendor_name": merchant_name,
                "category_name": product.product_category.name,
                "sub_category_name": product.product_category.product_sub_categories[0].name if product.product_category.product_sub_categories else ""
            }
            product_shop_data.append(data)

        return jsonify({
            "message": "All Pending products information",
            "data": product_shop_data,
            "total_pending_products": total_pending_products,
            "total_pages": int(total_no_of_pages)
        }), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@product.route("/<product_id>", methods=["GET"])
@admin_required(request=request)
def get_product(user_id : UUID, product_id : UUID) -> dict:
    """
    Get product information.

    Args:
        user_id (UUID): The ID of the user.
        product_id (UUID): The ID of the product.

    Returns:
        dict: A dictionary containing the following information:
            - "message" (str): The message indicating the success of the operation.
            - "data" (list): A list of dictionaries containing the product information.

    Raises:
        ValidationError: If there is a validation error.
        Exception: If there is an internal server error.

    Examples:
        # Example 1: Get product by ID
        get_product(user_id, product_id)
    """
    product_id = IdSchema(id=product_id)
    product_id = product_id.id
    try:
        product = Product.query.filter_by(id=product_id).first()

        product_shop_data = []

        def check_product_status(product):
            if product.admin_status == "suspended":
                return "Sanctioned"
            if (
                product.admin_status in ["approved"]
                and product.is_deleted == "active"
            ):
                return "Active"
            if product.is_deleted == "temporary":
                return "Deleted"

        if not product:
            return jsonify({"error": "Not found", "message": "Product Not Found"}), 404

        shop = Shop.query.filter_by(id=product.shop_id).first()  #object of the shop
        merchant_name = f"{shop.user.first_name} {shop.user.last_name}"
        data = {
            "product_image": image_gen(product.id),
            "vendor_profile_pic":  vendor_profile_image(shop.merchant_id),   
            "admin_status": product.admin_status,
            "category_id": product.category_id,
            "user_id": product.user_id,
            "createdAt": product.createdAt,
            "currency": product.currency,
            "description": product.description,
            "discount_price": product.discount_price,
            "product_id": product.id,
            "is_deleted": product.is_deleted,
            "is_published": product.is_published,
            "product_name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "rating_id": product.rating_id,
            "shop_id": product.shop_id,
            "tax": product.tax,
            "updatedAt": product.updatedAt,
            "product_status": check_product_status(product),
            "shop_name": shop.name,
            "vendor_name": merchant_name,
            "category_name": product.product_category.name,
            "sub_category_name": product.product_category.product_sub_categories[0].name if product.product_category.product_sub_categories else None
        }
        product_shop_data.append(data)

        return jsonify(
            {
                "message": "product successfull retrieved",
                "data": product_shop_data,
            }
        ), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@product.route("/<product_id>/sanction", methods=["PATCH"])
@admin_required(request=request)
def to_sanction_product(user_id : UUID, product_id : UUID) -> dict:
    """
        Sanction a product.

        Args:
            user_id (UUID): The ID of the user.
            product_id (UUID): The ID of the product to be sanctioned.

        Returns:
            dict: A dictionary containing the following information:
                - "data" (dict): A dictionary containing the formatted product information.
                - "message" (str): The message indicating the success of the sanctioning action.

        Raises:
            ValidationError: If there is a validation error.

        Examples:
            # Example 1: Sanction a product
            to_sanction_product(user_id, product_id)
        """
    product_id = IdSchema(id=product_id)
    product_id = product_id.id

    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return jsonify(
            {"error": "Product Not Found", "message": "Product does not exist"}
        ), 404

    if  product.admin_status == "suspended":
        return jsonify(
            {
                "error": "Conflict",
                "message": "Product has already been sanctioned"
            }
        ), 409

    # Start a transaction
    db.session.begin_nested()

    # Update product attributes
    product.admin_status = "suspended"

    # Commit the transaction
    db.session.commit()

    # ========================Log and notify the owner of the sanctioning action====================
    try:
        register_action_d(user_id, "Product Sanction", product_id)
        notify(action="sanction", product_id=product_id)
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
    # ==============================================================================================

    return jsonify(
        {
            "data": product.format(),
            "message": "Product sanctioned successfully",
        }
    ), 200


@product.route("/products-statistics", methods=["GET"])
@admin_required(request=request)
def get_product_statistics(user_id : UUID) -> dict:
    """
    Get product statistics.

    Args:
        user_id (UUID): The ID of the user.

    Returns:
        dict: A dictionary containing the following information:
            - "status" (str): The status indicating the success of the operation.
            - "product_statistics" (dict): A dictionary containing the product statistics:
                - "total_products" (int): The total number of products.
                - "total_sanctioned_products" (int): The total number of sanctioned products.
                - "total_deleted_products" (int): The total number of deleted products.

    Raises:
        Exception: If there is a bad request or an error occurs while retrieving the product statistics.

    Examples:
        # Example 1: Get product statistics
        get_product_statistics(user_id)
    """

    try:
        all_products = Product.query.count()
        sanctioned_products = Product.query.filter_by(
            admin_status="suspended", is_deleted="temporary"
        ).count()
        deleted_products = Product.query.filter_by(
            is_deleted="temporary").count()

        statistics = {
            "total_products": all_products,
            "total_sanctioned_products": sanctioned_products,
            "total_deleted_products": deleted_products,
        }

        return jsonify({"status": "Success", "product_statistics": statistics}), 200

    except Exception as exc:
        return jsonify(
            {
                "error": "Bad request",
                "message": "Something went wrong while retrieving product statistics: {exc}",
            }
        ), 400

@product.route("/<product_id>/restore", methods=["PATCH"])
@admin_required(request=request)
def to_restore_product(user_id : UUID, product_id : UUID ) -> dict:
    """
    Restore a temporarily deleted product.

    Args:
        user_id (UUID): The ID of the user.
        product_id (UUID): The ID of the product to be restored.

    Returns:
        dict: A dictionary containing the following information:
            - "message" (str): The message indicating the success of the restoration.
            - "data" (dict): A dictionary containing the formatted product information.

    Raises:
        ValidationError: If there is a validation error.
        Exception: If there is a bad request or an error occurs while performing the restoration action.

    Examples:
        # Example 1: Restore a product
        to_restore_product(user_id, product_id)
    """
    product_id = IdSchema(id=product_id)
    product_id = product_id.id

    try:
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return jsonify(
                {
                    "error": "Product Not Found",
                    "message": " Product Already deleted",
                }
            ), 404

        if product.is_deleted == "temporary":
            product.is_deleted = "active"
            db.session.commit()


            # ========================Log and notify the owner of the restored action====================
            try:
                register_action_d(user_id, "Product Restored", product_id)
            except Exception as error:
                logger.error(f"{type(error).__name__}: {error}")
            # ==============================================================================================


            return jsonify(
                {
                    'message': 'product restored successfully',
                    "data": product.format()
                }
            ), 201
        else:
            return jsonify(
                {
                    "message": "product is not marked as deleted",
                    "error": "conflict"
                }
            ), 409
    except Exception as exc:
        logger.error(f"{type(exc).__name__}: {exc}")
        return jsonify(
            {
                "error": "Bad request",
                "message": "Something went wrong while performing this Action",
            }
        ), 400


@product.route("/<product_id>/soft-delete", methods=["DELETE"])
@admin_required(request=request)
def temporary_delete(user_id : UUID, product_id: UUID) -> None:
    """
    Temporarily delete a product.

    Args:
        user_id (UUID): The ID of the user.
        product_id (UUID): The ID of the product to be temporarily deleted.

    Returns:
        None

    Raises:
        ValidationError: If there is a validation error.
        Exception: If there is an internal server error.

    Examples:
        # Example 1: Temporarily delete a product
        temporary_delete(user_id, product_id)
    """
    select_query = """
                        SELECT * FROM public.product
                        WHERE id=%s;"""

    delete_query = """UPDATE product
                        SET is_deleted = 'temporary'
                        WHERE id = %s;"""
    
    product_id = IdSchema(id=product_id)
    product_id = product_id.id
    try:
        with Database() as db:
            db.execute(select_query, (product_id,))
            selected_product = db.fetchone()
            if not selected_product:
                return jsonify({"error": "Not Found", "message": "Product not found"}), 404
            if selected_product[11] == "temporary":
                return jsonify(
                    {
                        "error": "Conflict",
                        "message": "Action already carried out on this Product",
                    }
                ), 409

            db.execute(delete_query, (product_id,))
            if request.headers.get("Content-Type") == "application/json":
                # Catch the error for non-existent JSON payload and dependent logger
                try:
                    data = request.json()
                    reason = data.get("reason")
                    register_action_d(user_id, f"Temporary Deletion for Reason: {reason}", product_id)
                except Exception as error:
                    logger.error(f"{type(error).__name__}: {error}")

            try:
                register_action_d(user_id, "Temporary Deletion", product_id)
            except Exception as log_error:
                logger.error(f"{type(log_error).__name__}: {log_error}")

        return jsonify(
            {
                "message": "Product temporarily deleted",
                "data": None,
            }
        ), 204
    except Exception as error:
        logger.error(f"{type(error).__name__}: {error}")
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500


@product.route("/<product_id>/approve", methods=["PATCH"])
@admin_required(request=request)
def approve_product(user_id : UUID, product_id : UUID) -> dict:  
    """
    Approve a product.

    Args:
        user_id (UUID): The ID of the user.
        product_id (UUID): The ID of the product to be approved.

    Returns:
        None

    Raises:
        ValidationError: If there is a validation error.
        Exception: If there is an internal server error.

    Examples:
        # Example 1: Approve a product
        approve_product(user_id, product_id)
    """

    select_query = """
                        SELECT * FROM public.product
                        WHERE id=%s;"""

    approve_query = """UPDATE product
                        SET admin_status = 'approved'
                        WHERE id = %s;"""

    product_id = IdSchema(id=product_id)
    product_id = product_id.id
    try:
        with Database() as db:
            db.execute(select_query, (product_id,))
            selectedproduct = db.fetchone()
            if not selectedproduct:
                return jsonify({"error": "Not Found", "message": "Product not found"}), 404
            if selectedproduct[10] == "approved":
                return jsonify(
                    {
                        "error": "Conflict",
                        "message": "Action already carried out on this Product",
                    }
                ), 409
            

            db.execute(approve_query, (product_id,))
            db.execute(select_query, (product_id,))
            selected_product = db.fetchone()
        if selected_product:
            data = {
                "id": selected_product[0],
                "shop_id": selected_product[1],
                "name": selected_product[2],
                "description": selected_product[3],
                "quantity": selected_product[4],
                "category_id": selected_product[5],
                "user_id": selected_product[6],
                "price": float(selected_product[7]),
                "discount_price": float(selected_product[8]),
                "tax": float(selected_product[9]),
                "admin_status": selected_product[10],
                "is_deleted": selected_product[11],
                "rating_id": selected_product[12],
                "is published": selected_product[13],
                "currency": selected_product[14],
                "created_at": str(selected_product[15]),
                "updated_at": str(selected_product[16]),
            }

            try:
                register_action_d(user_id, "Product Approval", product_id)
                notify(action="unsanction", product_id=product_id)

            except Exception as log_error:
                logger.error(f"{type(log_error).__name__}: {log_error}")
        return jsonify(
            {
                "message": "Product approved successfully",
                  "data": data
            }
        ), 201

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@product.route("/<product_id>", methods=["DELETE"])
@admin_required(request=request)
def permanent_delete(user_id : UUID, product_id : UUID) -> None:
    """
        Permanently delete a product.

        Args:
            user_id (UUID): The ID of the user.
            product_id (UUID): The ID of the product to be permanently deleted.

        Returns:
            None

        Raises:
            ValidationError: If there is a validation error.
            Exception: If there is an internal server error.

        Examples:
            # Example 1: Permanently delete a product
            permanent_delete(user_id, product_id)
    """

    select_query = """
                        SELECT id FROM public.product
                        WHERE id =%s;"""
    delete_query = """DELETE FROM public.product 
                                WHERE id = %s; """

    product_id = IdSchema(id=product_id)
    product_id = product_id.id
    try:            
        with Database() as db:
            db.execute(select_query, (product_id,))
            deleteproduct = db.fetchone()
            if not deleteproduct:
                return jsonify({"error": "Not Found", "message": "Product not found"}), 404
            db.execute(delete_query, (product_id,))
            try:
                register_action_d(user_id, "Permanent Product Deletion", product_id)
                notify(action="deletion", product_id=product_id)

            except Exception as log_error:
                logger.error(f"{type(log_error).__name__}: {log_error}")
        return jsonify({
            "message": "Product Permanently Deleted from the Database",
            "data": None
        }), 204
    
    except Exception as e:
        return jsonify(
            {
                "error": "Internal Server Error",
                "message": "we are currently experiencing a downtime with this feature"
            }
        ), 500


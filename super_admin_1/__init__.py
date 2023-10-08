from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
from super_admin_1.config import App_Config

db = SQLAlchemy()

def create_app():
    # Initialize Flask
    app = Flask(__name__)
    app.config.from_object(App_Config)
    if app.config["SQLALCHEMY_DATABASE_URI"]:
        print(f"using db")

    # Initialize CORS
    CORS(app, supports_credentials=True)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Import and register blueprints
    from super_admin_1.shop.unban_vendor import unban_vendor_blueprint
    from super_admin_1.shop.del_shop import del_shop
    from super_admin_1.shop.shop_activity import events
    from super_admin_1.shop.ban_vendor import shop as ban_vendor_blueprint
    from super_admin_1.products.restore_product import restore_product, create_product, delete_product
    from super_admin_1.products.delete_product import product_delete
    from .shop.ban_vendor import shop as shop_blueprint

    app.register_blueprint(del_shop, url_prefix='/api/del_shop')
    app.register_blueprint(events, url_prefix='/api/shop_activity')
    app.register_blueprint(ban_vendor_blueprint, url_prefix='/api/shop')
    app.register_blueprint(unban_vendor_blueprint, url_prefix='/api/shop/unban_vendor')
    app.register_blueprint(restore_product)
    app.register_blueprint(create_product)
    app.register_blueprint(delete_product)
    app.register_blueprint(product_delete)
    app.register_blueprint(shop_blueprint, url_prefix='/api/shop')

    # Create db tables from models if they do not exist
    with app.app_context():
        db.create_all()

    return app

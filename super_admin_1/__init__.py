from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
from super_admin_1.config import App_Config


db = SQLAlchemy()


def create_app():
    """
    Create a new instance of the app with the given configuration.

    :param config_class: configuration class
    :return: app
    """
    # Initialize Flask-

    app = Flask(__name__)
    app.config.from_object(App_Config)
    if app.config["SQLALCHEMY_DATABASE_URI"]:
        print(f"using db")

    # Initialize CORS
    CORS(app, supports_credentials=True)

    # Initialize SQLAlchemy
    db.init_app(app)



    # Import shop blueprint
    from super_admin_1.shop.routes import shop as shop_blueprint
    from super_admin_1.shop.del_shop import del_shop
    from super_admin_1.products.delete_product import product_delete

    # imports blueprints
    from super_admin_1.shop.del_shop import del_shop

    # register blueprints
    app.register_blueprint(del_shop)
    app.register_blueprint(product_delete)


    # imports blueprints

    # Testing db purpose
    # from super_admin_1.models.shop_log import ShopLog
    from super_admin_1.shop.shop_activity import events

    # register blueprints
    app.register_blueprint(events)

    # Register blueprints
    from .shop.ban_vendor import shop

    app.register_blueprint(shop, url_prefix='/api/shop')


    # Register the shop Blueprint
    app.register_blueprint(shop_blueprint)
    app.register_blueprint(del_shop)
    
    # create db tables from models if not exists
    with app.app_context():
        db.create_all()

    return app

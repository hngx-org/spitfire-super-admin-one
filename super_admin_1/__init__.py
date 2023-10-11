from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
from super_admin_1.config import App_Config
from flasgger import Swagger
import yaml

db = SQLAlchemy()


# Create an instance of Swagger
swagger = Swagger()

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

    # Load Swagger content from the file
    with open('swagger_config.yaml', 'r') as file:
        swagger_config = yaml.load(file, Loader=yaml.FullLoader)
    # Initialize Flasgger with the loaded Swagger configuration
    Swagger(app, template=swagger_config)

    # Initialize SQLAlchemy
    db.init_app(app)

    # imports blueprints
    from super_admin_1.shop.del_shop import del_shop
    from super_admin_1.shop.restore_shop import restore_shop_bp
    from super_admin_1.shop.unban_vendor import shop_blueprint
    from super_admin_1.shop.shop_activity import events
    from super_admin_1.shop.ban_vendor import shop
    from super_admin_1.products.routes import product
    from super_admin_1.shop import deleted_vendors

    # register blueprint
    app.register_blueprint(del_shop)
    app.register_blueprint(restore_shop_bp)
    app.register_blueprint(events)
    app.register_blueprint(shop, url_prefix='/api/shop')
    app.register_blueprint(shop_blueprint)
    app.register_blueprint(product)
    app.register_blueprint(deleted_vendors)

    
    # create db tables from models if not exists
    with app.app_context():
        db.create_all()

    return app

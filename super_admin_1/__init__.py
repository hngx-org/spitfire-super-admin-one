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
    with open("swagger_config.yaml", "r") as file:
        swagger_config = yaml.load(file, Loader=yaml.FullLoader)
    # Initialize Flasgger with the loaded Swagger configuration
    Swagger(app, template=swagger_config)

    # Initialize SQLAlchemy
    db.init_app(app)

    # imports blueprints
    from super_admin_1.shop.routes import shop
    from super_admin_1.logs.routes import logs
    from super_admin_1.products.routes import product
    from super_admin_1.shop.func_helpers import test
    from super_admin_1.errors.handlers import error
    from super_admin_1.notification.routes import notification
    from health import health

    # register blueprint
    app.register_blueprint(error)
    app.register_blueprint(shop)
    app.register_blueprint(logs)
    app.register_blueprint(product)
    app.register_blueprint(notification)
    app.register_blueprint(health)

    # create db tables from models if not exists
    with app.app_context():
        db.create_all()

    return app

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
    from super_admin_1.shop.routes import shop, logs
    from super_admin_1.products.routes import product
<<<<<<< HEAD
    from super_admin_1.shop.temp_deleted_vendors import deleted_vendors
=======
    from super_admin_1.shop.func_helpers import test

>>>>>>> 259c32c056a31f0567795f3039f6e54807f07c85

    # register blueprint
    app.register_blueprint(shop)
    app.register_blueprint(logs)
    app.register_blueprint(product)
<<<<<<< HEAD
    app.register_blueprint(deleted_vendors)
=======
    app.register_blueprint(test)
>>>>>>> 259c32c056a31f0567795f3039f6e54807f07c85

    
    # create db tables from models if not exists
    with app.app_context():
        db.create_all()

    return app

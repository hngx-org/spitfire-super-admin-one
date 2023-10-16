import logging, os

from flask import Blueprint


ERROR_LOGS_FILE = os.getenv(
    "ERROR_LOGS_FILE",
    os.path.join(os.path.abspath("."), "logs", "health_errors.log")
)

with open(ERROR_LOGS_FILE, "w+t") as f:
    pass

health = Blueprint("health", __name__, url_prefix="/api/admin/health")
health_logger = logging.getLogger("health_check")
health_logger.setLevel(logging.ERROR)
health_logger.addHandler(logging.FileHandler(ERROR_LOGS_FILE))

from .routes import *  # noqa

from flask import Blueprint
import logging


health = Blueprint("health", __name__, url_prefix="/api/admin/health")
health_logger = logging.getLogger("health_check")
health_logger.setLevel(logging.ERROR)

from .routes import *  # noqa

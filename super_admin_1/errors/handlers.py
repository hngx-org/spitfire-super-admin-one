
from flask import Blueprint, jsonify

error = Blueprint("error", __name__)


class CustomError(Exception):
    def __init__(self, error, code, message):
        self.error = error
        self.code = code
        self.message = message




@error.app_errorhandler(CustomError)
def resource_not_found(err):
    return (
        jsonify({"error": err.error, "message": err.message, "status": False}),
        err.code,
    )

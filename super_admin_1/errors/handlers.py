from flask import Blueprint, jsonify
from pydantic import ValidationError

error = Blueprint("error", __name__)


class CustomError(Exception):
    """Exception class for custom errors"""

    def __init__(self, error, code, message):
        """constructor for custom error class

        Args:
            error (_type_): Error Name
            code (_type_): HTTP error code
            message (_type_): error message
        """
        self.error = error
        self.code = code
        self.message = message



@error.app_errorhandler(CustomError)
def custom_error(error):
    """app error handler for custom errors"""
    return (
        jsonify({"error": error.error, "message": error.message}),
        error.code,
    )

@error.app_errorhandler(ValidationError)
def raise_validation_error(error):
    """app error handler for pydantic validation errors"""
    msg = []
    for err in error.errors():
        msg.append({
            "field": err["loc"][0],
            "error": err["msg"]
        })
    return (
        jsonify({"error": "Bad Request", "message": msg}),
        400,
    )

@error.app_errorhandler(400)
def bad_request(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return jsonify({"error": error.name, "message": error.description}), 400


@error.app_errorhandler(401)
def Unauthorized(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return jsonify({"error": error.name, "message": error.description}), 401


@error.app_errorhandler(403)
def Forbidden(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return jsonify({"error": error.name, "message": error.description}), 403


@error.app_errorhandler(404)
def resource_not_found(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return jsonify({"error": error.name, "message": error.description}), 404


@error.app_errorhandler(405)
def method_not_allowed(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return (
        jsonify({"error": error.name, "message": error.description}),
        405,
    )


@error.app_errorhandler(422)
def cant_process(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return jsonify({"error": error.name, "message": error.description}), 422


# pylint: disable=function-redefined
@error.app_errorhandler(429)
def cant_process(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return jsonify({"error": error.name, "message": error.description}), 429


@error.app_errorhandler(500)
def server_error(error):
    """_summary_

    Args:
        error (_type_): _description_

    Returns:
        _type_: _description_
    """
    return jsonify({"error": error.name, "message": "Its not you its us"}), 500

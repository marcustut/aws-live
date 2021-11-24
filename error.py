from flask import Blueprint, jsonify
from flask.helpers import make_response
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound
from jsonschema import ValidationError

blueprint = Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(NotFound)
def resource_not_found(e: NotFound):
    return ({"error": e.description}, e.code, e.response)


@blueprint.app_errorhandler(InternalServerError)
def internal_server_error(e: InternalServerError):
    return ({"error": e.description}, e.code, e.response)


@blueprint.app_errorhandler(BadRequest)
def bad_request(e: BadRequest):
    if isinstance(e.description, ValidationError):
        original_error = e.description
        return make_response(jsonify({"error": original_error.message}), 400)
    return ({"error": e.description}, e.code, e.response)


blueprint.register_error_handler(NotFound, resource_not_found)
blueprint.register_error_handler(InternalServerError, internal_server_error)
blueprint.register_error_handler(BadRequest, bad_request)

import logging
import sys
import traceback

from flask import Response, request
from flask.json import jsonify
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import HTTPException, BadRequest

from api import flask

# -------- Constants -----------
OPERATOR_OR = 'OR'
OPERATOR_AND = 'AND'
OPERATORS = [OPERATOR_AND, OPERATOR_OR]


# -------- API routes ----------

@flask.route("/users")
def get_users():
    latitude_input: str = request.args.get('latitude')
    longitude_input: str = request.args.get('longitude')
    city: str = request.args.get('city')
    operator: str = request.args.get('operator', default=OPERATOR_AND)

    # convert and validate input
    try:
        latitude = float(latitude_input) if latitude_input else None
        longitude = float(longitude_input) if longitude_input else None
    except ValueError:
        raise BadRequest('"latitude" and "longitude" need to be floats')
    if latitude and (latitude > 90 or latitude < -90):
        raise BadRequest('"latitude" needs to be a float between -90 and 90')
    if longitude and (longitude > 180 or longitude < -180):
        raise BadRequest('"longitude" needs to be a float between 180 and 180')
    if operator not in OPERATORS:
        raise BadRequest(f'"operator" needs to be one of: {OPERATORS}')
    if not (latitude and longitude) or city:
        raise BadRequest('Need to supply either "city", or "latitude" and "longitude"')

    return jsonify({})



# -------- System routes ----------

@flask.route("/healthcheck")
def healthcheck():
    """
    Execute a status check on API
    :return:
    """

    body = {'status': 'ok'}

    return jsonify(body)


@flask.errorhandler(Exception)
def json_exception_handler(error: Exception, message=None):
    """
    Handle exceptions and transform them into JSON
    :param message:
    :param report:
    :param error:
    :return:
    """

    # log the regular way first
    logging.exception(error)

    # base message
    body = {
        'message': message if message else error.__class__.__name__
    }

    # debugging info
    if flask.debug:
        body['message'] = str(error)
        body['type'] = error.__class__.__name__
        body['stack'] = []
        for frame in traceback.extract_tb(sys.exc_info()[2]):
            body['stack'].append({
                'file': frame.filename,
                'line': frame.lineno,
                'name': frame.name,
            })

    response: Response = jsonify(body)
    response.status_code = 500

    return response


@flask.errorhandler(HTTPException)
def json_http_exception_handler(error: HTTPException):
    """
    For HTTP exceptions, we change the status code
    and always display the exception message
    :param error:
    :return:
    """
    response = json_exception_handler(error, message=error.description)
    response.status_code = error.code
    return response

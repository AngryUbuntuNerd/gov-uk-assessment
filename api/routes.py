import logging
import sys
import traceback
from typing import Optional

from flask import Response, request
from flask.json import jsonify
from werkzeug.exceptions import HTTPException, BadRequest

from api import flask
from api.repositories import UserRepository


# -------- Constants -----------

OPERATOR_OR = 'OR'
OPERATOR_AND = 'AND'
OPERATORS = [OPERATOR_AND, OPERATOR_OR]
RANGE_DEFAULT = 10.0


# -------- API routes ----------

@flask.route("/users")
def get_users():

    user_repository = UserRepository()

    # read request input
    latitude_input: Optional[str] = request.args.get('latitude')
    longitude_input: Optional[str] = request.args.get('longitude')
    range_input: str = request.args.get('range', default=RANGE_DEFAULT)
    city: Optional[str] = request.args.get('city')
    operator: str = request.args.get('operator', default=OPERATOR_OR)

    # convert and validate input
    try:
        latitude = float(latitude_input) if latitude_input else None
        longitude = float(longitude_input) if longitude_input else None
        range = float(range_input)
    except ValueError:
        raise BadRequest('"latitude", "longitude" and "range" need to be floats')
    if latitude and (latitude > 90 or latitude < -90):
        raise BadRequest('"latitude" needs to be a float between -90 and 90')
    if longitude and (longitude > 180 or longitude < -180):
        raise BadRequest('"longitude" needs to be a float between 180 and 180')
    if range < 0:
        raise BadRequest('"range" needs to a positive number')
    if operator not in OPERATORS:
        raise BadRequest(f'"operator" needs to be one of: {OPERATORS}')
    if not (latitude and longitude) or city:
        raise BadRequest('Need to supply either "city", or "latitude" and "longitude"')

    # fetch users
    city_users = set()
    ranged_users = set()
    if city:
        city_users.update(user_repository.fetch_city_users(city))
    if latitude and longitude:
        all_users = user_repository.fetch_users()
        ranged_users.update(filter(lambda user: user.is_in_range(latitude, longitude, range_input), all_users))

    # combine users logically
    if city and latitude and longitude and operator == OPERATOR_AND:
        users = city_users.intersection(ranged_users)
    else:
        users = city_users.union(ranged_users)

    users_as_dicts = [user.__dict__ for user in users]
    return jsonify(users_as_dicts)


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

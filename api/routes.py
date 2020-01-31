import logging
import sys
import traceback
from typing import Optional

from flask import Response, request
from flask.json import jsonify
from werkzeug.exceptions import HTTPException, BadRequest

from api import flask
from api.models import Coordinate
from api.repositories import UserRepository


# -------- Constants -----------

OPERATOR_OR = 'OR'
OPERATOR_AND = 'AND'
OPERATORS = [OPERATOR_AND, OPERATOR_OR]
RANGE_DEFAULT = '10.0'


# -------- API routes ----------

@flask.route("/")
@flask.route("/users")
def get_users():

    user_repository = UserRepository()

    # read request input
    latitude: Optional[str] = request.args.get('latitude')
    longitude: Optional[str] = request.args.get('longitude')
    range_input: str = request.args.get('range', default=RANGE_DEFAULT)
    city: Optional[str] = request.args.get('city')
    operator: str = request.args.get('operator', default=OPERATOR_OR)

    # convert and validate input
    try:
        coordinate = Coordinate(latitude, longitude)
        range = float(range_input)
    except ValueError:
        raise BadRequest('"latitude", "longitude" and "range" need to be floats')
    if coordinate and not coordinate.is_valid():
        raise BadRequest('"latitude" and "longitude" need to form a valid coordinate')
    if range < 0:
        raise BadRequest('"range" needs to a positive number')
    if operator not in OPERATORS:
        raise BadRequest(f'"operator" needs to be one of: {OPERATORS}')
    if not city and not coordinate:
        raise BadRequest('Need to supply either "city", or "latitude" and "longitude"')

    # fetch users
    city_users = set()
    ranged_users = set()
    if city:
        city_users = set(user_repository.fetch_city_users(city))
    if coordinate:
        all_users = user_repository.fetch_users()
        ranged_users = set(filter(lambda user: user.is_in_range(coordinate, range), all_users))

    # combine users logically
    if city and coordinate and operator == OPERATOR_AND:
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

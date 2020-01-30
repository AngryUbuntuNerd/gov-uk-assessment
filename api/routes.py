import logging
import sys
import traceback

from flask import Response
from flask.json import jsonify
from werkzeug.exceptions import HTTPException

from api import flask


# -------- API routes ----------

# @flask.route("/my-route")
# def my_route():
#     ...


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

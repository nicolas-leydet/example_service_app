from flask import jsonify


def _response(status_code, payload):
    response = jsonify(payload)
    response.status_code = status_code
    return response


def success(payload=None):
    return _response(status_code=200, payload=payload or {})


def created(payload=None):
    return _response(status_code=201, payload=payload or {})


def does_not_exist():
    return _response(
        status_code=404,
        payload={'errors': [{'code': 'DOES_NOT_EXIST'}]})


def server_error(exception):
    return _response(
        status_code=500,
        payload={'errors': [{'code': 'SERVER_ERROR'}]})

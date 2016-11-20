from flask import request
from werkzeug.exceptions import BadRequest

from simple_api.http_helper import (
    success,
    created,
    does_not_exist,
    server_error,
    invalid_json,
)
from simple_api.api import api
from simple_api.mongo_storage import storage


# TODO decouple service and flask implementation
@api.route('/objects', methods=['POST'])
def post_object():
    try:
        data = request.get_json(force=True)
    except BadRequest:
        return invalid_json()

    try:
        new_id = storage.create(data)
        return created({'id': new_id})
    except Exception as e:
        return server_error(e)


@api.route('/objects', methods=['GET'])
def list_object():
    try:
        result = storage.find()
        response = success({'data': result})
        return response
    except Exception as e:
        return server_error(e)


@api.route('/objects/<string:id>')
def get_object(id):
    try:
        return success(storage.read(id))
    except KeyError as e:
        return does_not_exist()
    except Exception as e:
        return server_error(e)


@api.route('/objects/<string:id>', methods=['DELETE'])
def delete_object(id):
    try:
        storage.delete(id)
        return success({})
    except KeyError as e:
        return does_not_exist()
    except Exception as e:
        return server_error(e)


@api.route('/objects/<string:id>', methods=['PUT'])
def put_object(id):
    try:
        data = request.get_json(force=True)
    except BadRequest:
        return invalid_json()

    try:
        return success(storage.update(id, data))
    except KeyError as e:
        return does_not_exist()
    except Exception as e:
        return server_error(e)

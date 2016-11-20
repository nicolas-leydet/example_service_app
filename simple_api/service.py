from flask import request

from simple_api.http_helper import (
    success,
    created,
    does_not_exist,
    server_error,
)
from simple_api.api import api
from simple_api.storage import db


@api.route('/objects', methods=['POST'])
def post_object():
    try:
        data = request.get_json(force=True)
        data['id'] = db.index
        db.table[db.index] = data
    except Exception:
        return server_error()

    response = created({'id': db.index})
    db.index += 1

    return response


@api.route('/objects', methods=['GET'])
def list_object():
    try:
        return success({'data': list(db.table.values())})
    except Exception as e:
        return server_error()


@api.route('/objects/<int:id>')
def get_object(id):
    try:
        return success(db.table[id])
    except KeyError as e:
        return does_not_exist()
    except Exception as e:
        return server_error()


@api.route('/objects/<int:id>', methods=['DELETE'])
def delete_object(id):
    try:
        del db.table[id]
    except KeyError as e:
        return does_not_exist()
    except Exception as e:
        return server_error()

    return success({})


@api.route('/objects/<int:id>', methods=['PUT'])
def put_object(id):
    try:
        data = request.get_json()
        db.table[id]
        db.table[id] = data
    except KeyError as e:
        return does_not_exist()
    except Exception as e:
        return server_error()

    return success({})

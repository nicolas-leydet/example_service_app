from flask import Flask, jsonify, request

from simple_api.http import (
    success,
    created,
    does_not_exist,
    server_error
)


app = Flask(__name__)

class DB(object):
    def __init__(self):
        self.table = {}
        self.index = 0

db = DB()


@app.route('/objects', methods=['POST'])
def post_object():

    try:
        data = request.get_json()
        db.table[db.index] = data
    except Exception as e:
        return server_error()

    response = created({'id': db.index})
    db.index += 1

    return response


@app.route('/objects', methods=['GET'])
def list_object():
    try:
        return success({'data': list(db.table.values())})
    except Exception as e:
        return server_error()


@app.route('/objects/<int:id>')
def get_object(id):
    try:
        return success(db.table[id])
    except IndexError as e:
        return does_not_exist()
    except Exception as e:
        return server_error()


@app.route('/objects/<int:id>', methods=['DELETE'])
def delete_object(id):
    try:
        del db.table[id]

    except Exception as e:
        return server_error()

    return success({})


@app.route('/objects/<int:id>', methods=['PUT'])
def put_object(id):
    try:
        data = request.get_json()
        old_data = db.table[id]
        db.table[id] = data
    except IndexError as e:
        return does_not_exist()
    except Exception as e:
        return server_error()

    return success({})


def get_api():
    return app, db


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

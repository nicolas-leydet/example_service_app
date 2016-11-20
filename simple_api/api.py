from flask import Flask


api = Flask(__name__)


import simple_api.simple_service  # noqa


def get_api():
    return api

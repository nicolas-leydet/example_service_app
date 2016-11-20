from flask import Flask


api = Flask(__name__)


import simple_api.service  # noqa


def get_api():
    return api

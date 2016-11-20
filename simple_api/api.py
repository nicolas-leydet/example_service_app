from flask import Flask


api = Flask(__name__)


import simple_api.service


def get_api():
    return api

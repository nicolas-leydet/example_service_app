from flask import Flask

from simple_api.helper.flask_service import register_service
from simple_api.knoggets import Knoggets


def create_api():
    api = Flask(__name__)
    register_service(api, Knoggets())
    return api

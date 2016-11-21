from flask import Flask

from knogget.helper.flask_service import register_service
from knogget.services.knoggets import Knoggets


def create_api():
    api = Flask(__name__)
    register_service(api, Knoggets())
    return api

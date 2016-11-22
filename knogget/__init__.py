from flask import Flask

from knogget.helper.flask_service import service_api


app = Flask(__name__)
api = service_api(app)

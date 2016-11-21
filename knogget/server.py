from gevent import monkey
monkey.patch_all()

from gevent.wsgi import WSGIServer  # noqa
from knogget.api import create_api   # noqa
from knogget.services.knoggets import Knoggets  # noqa


def run():
    api = create_api()
    Knoggets.storage.setup()

    http_server = WSGIServer(('', 5000), api)
    http_server.serve_forever()

if __name__ == '__main__':
    run()

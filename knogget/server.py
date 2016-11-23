import resource

from gevent.wsgi import WSGIServer
from gevent import monkey
monkey.patch_all()

from knogget import api   # noqa
from knogget.services.knoggets import Knoggets  # noqa


def run():
    resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 65536))

    http_server = WSGIServer(('', 5000), api)
    http_server.serve_forever()


if __name__ == '__main__':
    run()

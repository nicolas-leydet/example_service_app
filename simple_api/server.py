from simple_api.api import get_api
from simple_api.mongo_storage import storage


def run():
    # TODO add context manager
    storage.setup()
    get_api().run(host='0.0.0.0')
    storage.finalize()


if __name__ == '__main__':
    run()

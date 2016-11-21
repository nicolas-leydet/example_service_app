from simple_api.api import create_api
from simple_api.services.knoggets import Knoggets


def run():
    create_api().run(host='0.0.0.0')
    Knoggets.storage.setup()


if __name__ == '__main__':
    run()

from simple_api.api import get_api


def run():
    get_api().run(host='0.0.0.0')


if __name__ == '__main__':
    run()

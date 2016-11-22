import inspect

from flask import request
from werkzeug.exceptions import BadRequest

from knogget.helper.dependency import make_dependencies_lazy
from knogget.helper import http


def service_api(flask_app, decorator_name='http_service'):
    '''
    Add the `decorator_name` decorator to the flask app `flask_app`

    This decorator can be used to decorate service classes.
    Service classes public methods are wrapped in http managemnt code
    and mapped to api routes (using convention see register_service function)
    '''
    assert not hasattr(flask_app, decorator_name)
    setattr(flask_app, decorator_name, get_flask_service_decorator(flask_app))
    return flask_app


def get_flask_service_decorator(api):
    def flask_service_decorator(service_class):
        make_dependencies_lazy(service_class)
        register_service(api, service_class())
        return service_class
    return flask_service_decorator


# TODO manage non CRUD functions
def register_service(api, service):
    '''
    Register a route for each public methods of the service instance
    including CRUD and custom function.

    :param api: a flask apilication
    :param service: object whose public methods (by convention, not
    starting by _) are register in api's routes.
    '''
    endpoint_name = service.__class__.__name__.lower()

    url = '/{}'.format(endpoint_name)
    if hasattr(service, 'create'):
        func = create_wrapper(service.create)
        api.add_url_rule(url, view_func=func, methods=['POST'])
    if hasattr(service, 'find'):
        func = find_wrapper(service.find)
        api.add_url_rule(url, view_func=func, methods=['GET'])

    url = '/{}/<string:id>'.format(endpoint_name)
    if hasattr(service, 'update'):
        func = update_wrapper(service.update)
        api.add_url_rule(url, view_func=func, methods=['PUT'])
    if hasattr(service, 'delete'):
        func = delete_wrapper(service.delete)
        api.add_url_rule(url, view_func=func, methods=['DELETE'])
    if hasattr(service, 'read'):
        func = read_wrapper(service.read)
        api.add_url_rule(url, view_func=func, methods=['GET'])

    # FIXME Does not work
    # NOTE create problem when multiple service register
    # api.before_first_request(service.storage.setup)


def create_wrapper(create_func):
    def wrapped_create():
        try:
            data = request.get_json(force=True)
        except BadRequest:
            return http.invalid_json()

        try:
            new_id = create_func(data)
            return http.created({'id': new_id})
        except Exception as e:
            return http.server_error(e)
    return wrapped_create


def find_wrapper(find_func):
    def wrapped_find():
        try:
            data = request.get_json(force=True)
        except BadRequest:
            return http.invalid_json()

        query = data.get('query', None)
        offset = data.get('offset', None)
        limit = data.get('limit', None)

        try:
            result = find_func(query, offset, limit)
            return http.success({'data': result})
        except Exception as e:
            return http.server_error(e)
    return wrapped_find


def read_wrapper(read_func):
    def wrapped_read(id):
        try:
            return http.success(read_func(id))
        except KeyError as e:
            return http.does_not_exist()
        except Exception as e:
            return http.server_error(e)
    return wrapped_read


def delete_wrapper(delete_func):
    def wrapped_delete(id):
        try:
            delete_func(id)
            return http.success({})
        except KeyError as e:
            return http.does_not_exist()
        except Exception as e:
            return http.server_error(e)
    return wrapped_delete


def update_wrapper(update_func):
    def wrapped_update(id):
        try:
            data = request.get_json(force=True)
        except BadRequest:
            return http.invalid_json()

        try:
            return http.success(update_func(id, data))
        except KeyError as e:
            return http.does_not_exist()
        except Exception as e:
            return http.server_error(e)
    return wrapped_update

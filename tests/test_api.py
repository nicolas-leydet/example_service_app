import json
from string import Template

import pytest

from simple_api.api import get_api
from simple_api.mongo_storage import get_storage


multi_test = pytest.mark.parametrize


def pad_tuple(tuple_, size, default=None):
    return tuple_ + (default,) * (size - len(tuple_))


@pytest.fixture(scope='session')
def storage():
    storage = get_storage()
    storage.setup()
    yield storage
    storage.finalize()


# TODO make real unit tests if too slow
# TODO use parametrize to have 2 sets of test : one using the db,
# the other one a mock. Mark the db one as slow.
@pytest.fixture
def app(storage):
    api = get_api()
    storage.bulk_insert([{'txt': 'hello'}, {'txt': 'yoyo'}])
    yield api
    storage.clear()


@pytest.fixture
def existing_id(storage, app):
    return storage.create({'txt': 'I exist'})


def test_unknown_url(client):
    response = client.get('/not_exist')
    assert response.status_code == 404


def is_does_not_exist_error(payload):
    assert payload == {'errors': [{'code': 'DOES_NOT_EXIST'}]}


def has_invalid_json(payload):
    assert payload == {'errors': [{'code': 'INVALID_JSON'}]}


def return_an_id(payload):
    assert 'id' in payload
    assert payload['id'] is not None  # 0 accepted


def list_equal_for_field(expected, field):
    def partially_equal(payload):
        objects = payload['data']
        partial_result = [obj[field] for obj in objects]
        expected.sort()
        partial_result.sort()
        assert expected == partial_result
    return partially_equal


def equal_for_field(expected, field):
    def partially_equal(payload):
        assert expected == payload[field]
    return partially_equal


@multi_test('req, resp', [
    (  # Create
        ('post', '/objects', {'txt': 'yo'}),
        (201, [return_an_id]),
    ),
    (  # Create (invalid json)
        ('post', '/objects', '{"txt": yo}'),
        (400, [has_invalid_json]),
    ),
    (  # List
        ('get', '/objects'),
        (200, [list_equal_for_field(['I exist', 'hello', 'yoyo'],
                                    field='txt')]),
    ),
    (  # Read
        ('get', '/objects/$existing_id'),
        (200, [equal_for_field('I exist', field='txt')]),
    ),
    (  # Read (unknown id)
        ('get', '/objects/012345678901234567890123'),
        (404, [is_does_not_exist_error]),
    ),
    (  # Delete
        ('delete', '/objects/$existing_id'),
        (200, ),
    ),
    (  # Delete (unknown id)
        ('delete', '/objects/012345678901234567890123'),
        (404, [is_does_not_exist_error]),
    ),
    (  # Update
        ('put', '/objects/$existing_id', {'txt': 'yuyu'}),
        (200, {}),
    ),
    (  # Update (invalid json)
        ('put', '/objects/$existing_id', 'yoyo'),
        (400, [has_invalid_json]),
    ),
    (  # Update (unknown id)
        ('put', '/objects/012345678901234567890123', {'txt': 'yuyu'}),
        (404, [is_does_not_exist_error]),
    ),
])
def test_basic_call(client, req, resp, existing_id):
    method, url, payload = pad_tuple(req, 3)
    resp_code, payload_tests = pad_tuple(resp, 2, [])

    if payload is not None:  # not including {}
        if isinstance(payload, dict):
            payload = json.dumps(payload)

    url = replace_existing_id(url, existing_id)
    response = client.open(url, method=method, data=payload)

    assert response.status_code == resp_code
    for test_func in payload_tests:
        test_func(response.json)


def replace_existing_id(url, existing_id):
    return Template(url).substitute(existing_id=existing_id)

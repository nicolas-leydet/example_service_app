from string import Template
import json

import pytest

from knogget import api
from knogget.services.knoggets import Knoggets  # noqa


multi_test = pytest.mark.parametrize


@pytest.fixture(scope='session')
def app():
    return api


@pytest.fixture(scope='session')
def storage():
    storage = Knoggets.storage
    yield storage
    storage.terminate()


@pytest.fixture
def knoggets_fixture(storage):
    data = [{'txt': 'I exist'}, {'txt': 'hello'}, {'txt': 'yoyo'}]
    ids = storage.bulk_insert(data)
    yield ids
    storage.clear()


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
        ('POST /knoggets', {'txt': 'yo'}),
        (201, [return_an_id]),
    ),
    (  # Create (invalid json)
        ('POST /knoggets', '{"txt": yo}'),
        (400, [has_invalid_json]),
    ),
    (  # Find
        ('GET /knoggets', {}),
        (200, [list_equal_for_field(['I exist', 'hello', 'yoyo'],
                                    field='txt')]),
    ),
    (  # Read
        ('GET /knoggets/$id0', None),
        (200, [equal_for_field('I exist', field='txt')]),
    ),
    (  # Read (unknown id)
        ('GET /knoggets/012345678901234567890123', None),
        (404, [is_does_not_exist_error]),
    ),
    (  # Delete
        ('DELETE /knoggets/$id0', None),
        (200, []),
    ),
    (  # Delete (unknown id)
        ('DELETE /knoggets/012345678901234567890123', None),
        (404, [is_does_not_exist_error]),
    ),
    (  # Update
        ('PUT /knoggets/$id0', {'txt': 'yuyu'}),
        (200, []),
    ),
    (  # Update (invalid json)
        ('PUT /knoggets/$id0', 'yoyo'),
        (400, [has_invalid_json]),
    ),
    (  # Update (unknown id)
        ('PUT /knoggets/012345678901234567890123', {'txt': 'yuyu'}),
        (404, [is_does_not_exist_error]),
    ),
])
def test_basic_call(client, req, resp, knoggets_fixture):
    response = call_client(client, knoggets_fixture, *req)
    check_response(response, *resp)


def call_client(client, fixtures, path, payload=None, header=None):
    method, url = path.split(' ')
    url = replace_existing_id(url, fixtures)
    if payload is not None:
        if isinstance(payload, dict):
            payload = json.dumps(payload)

    return client.open(url, method=method, data=payload)


def check_response(response, expected_status_code, predicates):
    assert expected_status_code == response.status_code
    for predicate in predicates:
        predicate(response.json)


def replace_existing_id(url, fixtures):
    tokens = {
        'id{}'.format(index): obj_id
        for index, obj_id in enumerate(fixtures)
    }
    return Template(url).substitute(tokens)

import json

import pytest

from simple_api.api import get_api
from simple_api.storage import set_db_fixture


multi_test = pytest.mark.parametrize


def pad_tuple(tuple_, size, default=None):
    return tuple_ + (default,) * (size - len(tuple_))


@pytest.fixture()
def app():
    api = get_api()
    set_db_fixture({
        0: {'txt': 'hello'},
        1: {'txt': 'yoyo'},
    })
    return api


def test_unknown_url(client):
    response = client.get('/not_exist')
    assert response.status_code == 404


@multi_test('req, resp', [
    (  # Create
        ('post', '/objects', {'txt': 'yo'}),
        (201, {'id': 2}),
    ),
    (  # List
        ('get', '/objects'),
        (200, {'data': [{'txt': 'hello'}, {'txt': 'yoyo'}]}),
    ),
    (  # Read
        ('get', '/objects/1'),
        (200, {'txt': 'yoyo'}),
    ),
    (  # Read (no object)
        ('get', '/objects/3'),
        (404, {'errors': [{'code': 'DOES_NOT_EXIST'}]}),
    ),
    (  # Delete
        ('delete', '/objects/1'),
        (200, ),
    ),
    (  # Delete (no object)
        ('delete', '/objects/3'),
        (404, {'errors': [{'code': 'DOES_NOT_EXIST'}]}),
    ),
    (  # Update
        ('put', '/objects/0', {'txt': 'yuyu'}),
        (200, {}),
    ),
    (  # Update (no object)
        ('put', '/objects/3'),
        (404, {'errors': [{'code': 'DOES_NOT_EXIST'}]}),
    ),
    (  #
        ('get', '/objects/yo'),
        (404, ),
    ),
])
def test_basic_call(client, req, resp):
    method, url, payload = pad_tuple(req, 3)
    if payload is not None:  # not including {}
        payload = json.dumps(payload)

    resp_code, resp_payload = pad_tuple(resp, 2)

    response = client.open(url, method=method, data=payload)
    assert response.status_code == resp_code
    if resp_payload is not None:  # not including {}
        assert response.json == resp_payload
        # TODO try to use jsonschema.validate or marshmallow

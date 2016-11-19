import json

import pytest

from simple_api.api import get_api


multi_test = pytest.mark.parametrize

def pad_tuple(tuple_, size, default=None):
    return tuple_ + (default,) * (size - len(tuple_))


@pytest.fixture()
def app():
    app, db = get_api()
    db.table = {
        0: {'txt': 'hello'},
        1: {'txt': 'yoyo'},
    }
    db.index = 2
    return app


def test_unknown_url(client):
    response = client.get('/not_exist')
    assert response.status_code == 404


@multi_test('req, resp',[
    (
        ('post', '/objects', {'txt': 'yo'}),
        (201, {'id': 2}),
    ),
    (
        ('get', '/objects'),
        (200, {'data': [{'txt': 'hello'}, {'txt': 'yoyo'}]}),
    ),
    (
        ('get', '/objects/1'),
        (200, {'txt': 'yoyo'}),
    ),
    (
        ('delete', '/objects/1'),
        (200, ),
    ),
    (
        ('put', '/objects/0', {'txt': 'yuyu'}),
        (200, {}),
    ),
    (
        ('get', '/objects/yo'),
        (404, ),
    ),
])
def test_create_object(client, req, resp):
    method, url, payload = pad_tuple(req, 3)
    if payload != None: # not including {}
        payload = json.dumps(payload)

    resp_code, resp_payload = pad_tuple(resp, 2)

    response = client.open(url, method=method, data=payload)
    assert response.status_code == resp_code
    if resp_payload != None:
        assert response.json == resp_payload
        # TODO try to use jsonschema.validate or marshmallow

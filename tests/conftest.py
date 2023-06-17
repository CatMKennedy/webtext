# Contains fixtures for the tests. 

import os
import tempfile

import pytest
from appfiles import create_app
from appfiles.db import get_db, init_db

# Follows the patterns at: https://flask.palletsprojects.com/en/2.3.x/testing/ and
# https://flask.palletsprojects.com/en/2.3.x/tutorial/tests/.
# Four pytest fixtures are defined: 
# app() - creates a test Flask app and temporary test database
# client(app) - returns a Flask test_client for the app
# runner(app) - returns a test cli runner for the app
# auth(client) - creates some reusable auth methods for the test_client

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


# Class with login and logout methods to avoid repeated code in tests
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)

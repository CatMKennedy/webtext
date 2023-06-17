# Test the application factory

from appfiles import create_app


# Check that the config for the app is set to "TESTING"
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


# Test the simple "Hello world" page using the test_client (returned by a fixture)
def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
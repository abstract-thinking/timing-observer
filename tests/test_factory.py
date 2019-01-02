from app import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_ping(client):
    response = client.get('/ping/hello')
    assert response.data == b'Pong, hello!'
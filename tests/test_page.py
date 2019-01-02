def test_indices(client):
    response = client.get('/indices')
    assert b"MDAX" in response.data


def test_quotes(client):
    response = client.get('/quotes')
    assert b"MDAX" in response.data


def test_rsl(client):
    response = client.get('/rsl')
    assert b"MDAX" in response.data

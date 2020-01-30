from api import flask


def test_get_users_invalid_input_returns_400():
    client = flask.test_client()

    response = client.get("/users?longitude=nut")
    assert response.status_code == 400

    response = client.get("/users?latitude=nut")
    assert response.status_code == 400

    response = client.get("/users?range=nut")
    assert response.status_code == 400

    response = client.get("/users?latitude=100")
    assert response.status_code == 400

    response = client.get("/users?longitude=200")
    assert response.status_code == 400

    response = client.get("/users?operator=nut")
    assert response.status_code == 400

    response = client.get("/users")
    assert response.status_code == 400

    response = client.get("/users?latitude=80")
    assert response.status_code == 400

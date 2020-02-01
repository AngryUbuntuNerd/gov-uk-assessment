import os
from unittest.mock import patch, MagicMock

from api import flask
from api.models import User


os.environ['API_URL'] = 'http://something'


def test_get_users_returns_400_on_invalid_input():
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


@patch('api.repositories.UserRepository.fetch_city_users')
def test_get_users_returns_city_users(fetch_city_users_mock: MagicMock):
    city_users = [
        User(id=1, city='Magdeburg')
    ]
    fetch_city_users_mock.return_value = city_users

    client = flask.test_client()
    response = client.get("/users?city=Magdeburg")

    assert response.status_code == 200
    assert len(response.json) == 1


@patch('api.repositories.UserRepository.fetch_users')
def test_get_users_returns_ranged_users(fetch_users_mock: MagicMock):
    users = [
        User(id=1, city='Magdeburg', latitude=0, longitude=0),
        User(id=2, city='Bremen', latitude=10, longitude=10),
    ]
    fetch_users_mock.return_value = users

    client = flask.test_client()
    response = client.get("/users?latitude=0&longitude=0&range=10")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] == 1


@patch('api.repositories.UserRepository.fetch_users')
@patch('api.repositories.UserRepository.fetch_city_users')
def test_get_users_returns_city_or_ranged_users(fetch_city_users_mock: MagicMock,
                                                fetch_users_mock: MagicMock):
    users = [
        User(id=1, city='Magdeburg', latitude=0, longitude=0),
        User(id=2, city='Hamburg', latitude=10, longitude=10),
        User(id=3, city='Hamburg', latitude=0, longitude=0),
    ]
    city_users = [
        User(id=1, city='Magdeburg', latitude=0, longitude=0),
    ]
    fetch_users_mock.return_value = users
    fetch_city_users_mock.return_value = city_users

    client = flask.test_client()
    response = client.get("/users?latitude=0&longitude=0&range=10&city=Magdeburg&operator=OR")

    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["id"] in [1, 3]
    assert response.json[1]["id"] in [1, 3]


@patch('api.repositories.UserRepository.fetch_users')
@patch('api.repositories.UserRepository.fetch_city_users')
def test_get_users_returns_city_and_ranged_users(fetch_city_users_mock: MagicMock,
                                                 fetch_users_mock: MagicMock):
    users = [
        User(id=1, city='Magdeburg', latitude=0, longitude=0),
        User(id=2, city='Hamburg', latitude=10, longitude=10),
        User(id=3, city='Hamburg', latitude=0, longitude=0),
    ]
    city_users = [
        User(id=1, city='Magdeburg', latitude=0, longitude=0),
    ]
    fetch_users_mock.return_value = users
    fetch_city_users_mock.return_value = city_users

    client = flask.test_client()
    response = client.get("/users?latitude=0&longitude=0&range=10&city=Magdeburg&operator=AND")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] == 1

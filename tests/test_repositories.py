import requests_mock

from api.repositories import UserRepository


def test_user_repo_fetch_users_yields_model():
    user_repository = UserRepository('http://localhost')

    with requests_mock.Mocker() as mock:
        mock.get('http://localhost/users', json=[{'id': 1}, {'id': 2}])
        users = list(user_repository.fetch_users())

    assert len(users) == 2
    assert users[0].id == 1
    assert users[1].id == 2


def test_user_repo_fetch_city_users_yields_model():
    user_repository = UserRepository('http://localhost')

    with requests_mock.Mocker() as mock:
        mock.get('http://localhost/city/Bremen/users', json=[{'id': 1}, {'id': 2}])
        users = list(user_repository.fetch_city_users('Bremen'))

    assert len(users) == 2
    assert users[0].id == 1
    assert users[1].id == 2

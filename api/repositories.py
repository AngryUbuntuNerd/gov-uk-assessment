from typing import List, Generator

import requests

from api.models import User


class UserRepository:
    url = 'https://bpdts-test-app.herokuapp.com'

    def fetch_users(self) -> Generator[User]:
        response = requests.get(f'{self.url}/users')
        for user_data in response.json():
            user = User(**user_data)
            yield user

    def fetch_city_users(self, city: str) -> Generator[User]:
        response = requests.get(f'{self.url}/city/{city}/users')
        for user_data in response.json():
            user = User(**user_data)
            yield user

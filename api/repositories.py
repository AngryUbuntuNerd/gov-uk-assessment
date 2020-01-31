import os
from typing import Generator

import requests

from api.models import User


class UserRepository:

    def __init__(self):
        self.url = os.environ.get('API_URL')
        assert self.url, 'API_URL needs to be set'

    def fetch_users(self) -> Generator[User, None, None]:
        response = requests.get(f'{self.url}/users')
        for user_data in response.json():
            user = User(**user_data)
            yield user

    def fetch_city_users(self, city: str) -> Generator[User, None, None]:
        response = requests.get(f'{self.url}/city/{city}/users')
        for user_data in response.json():
            user = User(**user_data)
            yield user

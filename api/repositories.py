from typing import List

import requests

from api.models import User


class UserRepository:
    url = 'https://bpdts-test-app.herokuapp.com'

    def fetch_users(self) -> List[User]:
        users = []
        response = requests.get(f'{self.url}/users')
        for user_data in response.json():
            user = User(**user_data)
            users.append(user)
        return users

    def fetch_city_users(self, city: str):
        users = []
        response = requests.get(f'{self.url}/city/{city}/users')
        for user_data in response.json():
            user = User(**user_data)
            users.append(user)
        return users

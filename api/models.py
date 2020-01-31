from typing import Tuple

from geopy import distance


class Coordinate:
    def __init__(self, latitude, longitude):
        self.latitude = None
        self.longitude = None

        if latitude is not None:
            self.latitude = float(latitude)
        if longitude is not None:
            self.longitude = float(longitude)

    def __bool__(self):
        return self.latitude is not None and self.longitude is not None

    def is_valid(self):
        if not self:
            return False
        if not -90 <= self.latitude <= 90:
            return False
        if not -180 <= self.longitude <= 180:
            return False
        return True

    def to_tuple(self) -> Tuple[float, float]:
        return self.latitude, self.longitude


class User:
    def __init__(self, id: int, first_name: str = None, last_name: str = None, email: str = None,
                 ip_address: str = None, latitude: float = None, longitude: float = None, city: str = None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.ip_address = ip_address
        self.latitude = latitude
        self.longitude = longitude
        self.city = city

    def is_in_range(self, coordinate: Coordinate, range: float) -> bool:
        """
        Figure out if a user is within range (in miles) of a Coordinate
        :param coordinate:
        :param range:
        :return:
        """
        user_coordinate = Coordinate(self.latitude, self.longitude)
        if not user_coordinate.is_valid():
            return False

        distance_miles = distance.geodesic(coordinate.to_tuple(), user_coordinate.to_tuple()).miles
        return distance_miles <= range

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id

from geopy import distance


class User:
    def __init__(self, id: int, first_name: str, last_name: str, email: str,
                 ip_address: str, latitude: float, longitude: float, city: str = None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.ip_address = ip_address
        self.latitude = latitude
        self.longitude = longitude
        self.city = city

    def is_in_range(self, latitude: float, longitude: float, range: float) -> bool:
        """
        Figure out if a user is within range (in miles) of latitude/longitude
        :param latitude:
        :param longitude:
        :param range:
        :return:
        """
        user_coordinate = (self.latitude, self.longitude)
        other_coordinate = (latitude, longitude)
        distance_miles = distance.vincenty(user_coordinate, other_coordinate).miles
        return distance_miles <= range

    def __hash__(self):
        return hash(self.id)

    def to_json(self):
        return {

        }
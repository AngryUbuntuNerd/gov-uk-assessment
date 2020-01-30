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

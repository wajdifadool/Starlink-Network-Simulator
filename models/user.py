class User:
    def __init__(self , user_id :int , lat,lon, xyz ):
        self.user_id = user_id
        self.lat = lat
        self.lon = lon
        self.xyz = xyz

    def request_service(self, simulation: "Simulation") -> dict:
        """Simulate a user request for latency and bandwidth testing."""
        pass

    def __str__(self):
        return f"{self.user_id} , lat={self.lat}, lon={self.lon}, xyz={self.xyz}"

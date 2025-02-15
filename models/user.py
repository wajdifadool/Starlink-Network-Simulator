from models.satellite import Satellite
from skyfield.api import  wgs84
import  numpy as np

class User:

    def __init__(self , user_id :int , lat,lon):
        self.user_id = user_id
        self.lat = lat
        self.lon = lon
        self.xyz = self._calculate_xyz()

    def _calculate_xyz(self):
        # Use Skyfield's wgs84 to calculate XYZ in meters
        user_position = wgs84.latlon(latitude_degrees=self.lat, longitude_degrees=self.lon)
        user_xyz = user_position.itrs_xyz.km  # Convert from AU to km directly
        return  np.array(user_xyz)

    def request_service(self, simulation: "Simulation") -> dict:
        """Simulate a user request for latency and bandwidth testing."""
        pass

    def __str__(self):
        return f"{self.user_id} , lat={self.lat}, lon={self.lon}, xyz={self.xyz}"

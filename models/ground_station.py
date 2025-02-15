from models.satellite import Satellite
from skyfield.api import  wgs84
import  numpy as np

class GroundStation:
    def __init__(self, station_id: int,latitude: float, longitude: float ):
        self.station_id = station_id
        self.latitude = latitude
        self.longitude = longitude
        self.xyz = self._calculate_xyz()

    def _calculate_xyz(self):
        # Use Skyfield's wgs84 to calculate XYZ in meters
        ground_position = wgs84.latlon(latitude_degrees=self.latitude, longitude_degrees=self.longitude)
        ground_xyz = ground_position.itrs_xyz.km  # Convert from AU to km directly
        return  np.array(ground_xyz)

    def connect_to_satellite(self, satellite: Satellite) -> bool:
        """Check and establish a connection with a satellite."""
        pass



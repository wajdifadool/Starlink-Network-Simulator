from models.satellite import Satellite

class GroundStation:
    def __init__(self, station_id: int,latitude: float, longitude: float ):
        self.station_id = station_id
        self.latitude = latitude
        self.longitude = longitude


    def connect_to_satellite(self, satellite: Satellite) -> bool:
        """Check and establish a connection with a satellite."""
        pass



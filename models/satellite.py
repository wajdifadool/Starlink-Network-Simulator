
class Satellite:
    def __init__(self, satellite_id:int, latitude: float, longitude: float, altitude:float):
        self.satellite_id =  satellite_id
        self.latitude = latitude
        self.longitude= longitude
        self.altitude = altitude

    def is_above_threshold(self, threshold_km:float = 350 )->bool:
        """Check if the satellite is above a certain elevation."""
        return self.altitude > threshold_km

    def update_position(self, latitude: float, longitude: float):
        '''Upate the satellite position '''
        self.latitude = latitude
        self.longitude = longitude
        pass


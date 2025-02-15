import  numpy as np
import  re
class Satellite:

    def __init__(self, satellite_id:int, latitude: float, longitude: float, altitude:float ,sat_xyz, total_flow):
        self.satellite_id = satellite_id

        self.latitude = latitude if latitude is not None else None
        self.longitude = longitude if longitude is not None else None
        self.altitude = altitude if altitude is not None else None
        self.sat_xyz = np.array(sat_xyz) if sat_xyz is not None else None
        self.total_flow =  total_flow if total_flow is not  None else None
        self.connected_users = 0


    def is_above_threshold(self, threshold_km:float = 350 )->bool:
        """Check if the satellite is above a certain elevation."""
        return self.altitude > threshold_km


    def update_position(self, latitude: float, longitude: float):
        '''Upate the satellite position '''
        self.latitude = latitude
        self.longitude = longitude
        pass

    def __str__(self):
        return (
            f"Satellite ID: {self.satellite_id}, "
            f"Latitude: {self.latitude}, "
            f"Longitude: {self.longitude}, "
            f"Altitude: {self.altitude} km, "
            f"XYZ Coordinates: {self.sat_xyz}"
        )




from models.file_manager import  FileManager
from skyfield.api import load
from models.satellite import Satellite
import  numpy as np
from random import shuffle
from skyfield.api import  wgs84
import  time
from models.ground_station import  GroundStation
import  logging
import re
class GroundControl:
    """
    A class to manage satellite data and ground station information
     for tracking and operations.
    """
    def __init__(self):
        """
        Initializes the GroundControl instance by loading satellite and ground
        station data,and preparing dictionaries for satellite and ground
        station information.
        """
        print("Ground Control invoked")

        self.ts = load.timescale()
        self.file_manager = FileManager()

        self.my_satellites:[Satellite] = self._create_my_satellites()
        self.my_ground_stations:[GroundStation] = self._create_my_ground_stations()

    def _create_my_satellites(self):
        file_data = self.file_manager.load_tle_file_into_list()

        t = self.ts.now()
        temp = []
        for sat in file_data:
            geometry = sat.at(t)
            subpoint = geometry.subpoint()
            sat_elevation = subpoint.elevation.km

            if  700 > sat_elevation > 450  :
                sat_lat = subpoint.latitude.degrees
                sat_lng = subpoint.longitude.degrees

                sat_xyz = geometry.position.km
                # "Starlink-1008" will be now "1008", faster
                sat_name  = re.search(r"-(\d+)$",  sat.name).group(1)
                satellite = Satellite(sat_name, latitude=sat_lat, longitude=sat_lng, altitude=sat_elevation,
                                      sat_xyz=sat_xyz ,total_flow=None)
                temp.append(satellite)

        shuffle(temp)
        print(f"GroundControl::_create_my_satellites(), my_satellites count={len(temp)}")
        return temp

    def _create_my_ground_stations(self ):
        file_data = self.file_manager.load_ground_stations()
        # Create an array of GroundStation objects
        ground_stations = [GroundStation(name, coords["Latitude"], coords["Longitude"])
                           for name, coords in file_data.items()]

        print(f"GroundControl::_create_my_ground_stations(), my ground stations count={len(ground_stations)}")
        return ground_stations

    def refresh_my_satellites(self):
        """
        Refresh the list ( recalculate the satlites postion ased on the time )
        :return:
        """
        # print("Refrishng sats poytions ")
        self.my_satellites = self._create_my_satellites()


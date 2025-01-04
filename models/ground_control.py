from models.file_manager import  FileManager
from skyfield.api import load
from models.satellite import Satellite
import  numpy as np
from skyfield.api import  wgs84
import  time

import  logging
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
        self.ts = load.timescale()
        self.file_manager = FileManager()
        self.sats_raw = self.file_manager.load_tle_file_into_list()
        self.stats_list_clean = self.remove_unwanted_elevations()
        self.sats_dict_object_raw = self.create_sats_dict_object_raw()
        self.dict_name_lat_lng = self.create_sats_dict_lat_lng()

        self.ground_stations_raw = self.file_manager.load_ground_stations()
        self.ground_stations_long_lats = self.create_ground_stations_long_lats(self.ground_stations_raw)


    def create_ground_stations_long_lats(self , ground_stations_raw):
        """
        Extracts latitude and longitude information from raw ground station data
        :param ground_stations_raw: Raw ground station data.
        :return: tuple: Two lists containing latitudes and longitudes of
        the ground stations.
        """
        longs = [data["Longitude"] for data in self.ground_stations_raw.values()]
        lats = [data["Latitude"] for data in self.ground_stations_raw.values()]
        return lats, longs


    def remove_unwanted_elevations(self):
        """
        Filters satellites based on elevation, keeping only those above 400 km.
        :return: list: A list of satellites with elevations greater than 400 km.
        """
        t = self.ts.now()
        temp = []
        for sat in self.sats_raw:
            geometry = sat.at(t)

            subpoint = geometry.subpoint()
            elevation = subpoint.elevation.km
            if elevation > 400:
                temp.append(sat)
        logging.debug(f'number of satlites remaing are : {len(temp)}')
        return temp

    def create_sats_dict_object_raw(self):
        """
        Creates a dictionary of satellite objects with their name as the key.
        :return:dict: A dictionary mapping satellite names to Satellite objects.
        """
        t = self.ts.now()
        temp = dict()
        for sat in self.stats_list_clean:
            a = sat
            geometry = sat.at(t)
            subpoint = geometry.subpoint()
            lat = subpoint.latitude.degrees
            lng = subpoint.longitude.degrees
            elevation = subpoint.elevation.km
            name = sat.name
            sat_obj = Satellite(name, lat, lng, elevation)
            temp[name] = sat_obj
        return temp


    def create_sats_dict_lat_lng(self):
        """
        Creates a dictionary with satellite names as keys
        and their positions (latitude, longitude, and 3D position) as values.

        # THIS FUNCTION GET CALLED EACH X SECONDS WHEN WE UPDATE THE UI LAT AND LONG
        :return: dict: A dictionary mapping satellite names to their
        positional data.
        """
        t = self.ts.now()
        temp = dict()
        for sat in self.stats_list_clean:
            geometry = sat.at(t)
            subpoint = geometry.subpoint()
            lat = subpoint.latitude.degrees
            lng = subpoint.longitude.degrees
            name = sat.name

            # Save the Position object
            sat_xyz   =  geometry.position.km
            temp[name]  =  (lat , lng , sat_xyz )
        return temp

    def refresh_dict_lat_lng(self):
        """
        Refreshes the dictionary of satellite positional data by
         updating it with the latest values.
        :return:
        """
        self.dict_name_lat_lng = self.create_sats_dict_lat_lng()

    # TODO: CONSIDER calculating this in other thread, the need that each
    #  time we fetch the latest (lat , long) the data already avalebile
    #  and not blocking the ui
    def fetch_lat_long(self):
        """
        Fetches latitude and longitude values from the satellite position dictionary.
        :return: tuple: Two lists containing latitudes and longitudes of satellites.
        """
        lats = [obj[0] for obj in self.dict_name_lat_lng.values()]
        longs = [obj[1] for obj in self.dict_name_lat_lng.values()]
        return lats, longs
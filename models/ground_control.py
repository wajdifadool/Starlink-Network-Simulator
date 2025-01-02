from models.file_manager import  FileManager
from skyfield.api import load

from models.satellite import Satellite

import  numpy as np
from skyfield.api import  wgs84


class GroundControl:
    def __init__(self):
        self.ts = load.timescale()
        self.fm = FileManager()
        self.sats_raw = self.fm.load_satellites_file()
        self.sats = self.sats_list()
        self.sats_xy = self.stas_long_lats()

        self.gs_raw = self.fm.load_ground_stations()
        self.gs_xy = self.gs_long_lats()

    def stas_long_lats(self):
        lats = [float(sat.latitude) for sat in self.sats]
        longs = [float(sat.longitude) for sat in self.sats]
        return lats, longs

    def gs_long_lats(self):

        longs = [data["Longitude"] for data in self.gs_raw.values()]
        lats = [data["Latitude"] for data in self.gs_raw.values()]
        return lats, longs

    def sats_list(self):
        t = self.ts.now()
        temp = []
        for sat in self.sats_raw:
            geometry = sat.at(t)

            subpoint = geometry.subpoint()
            lat =subpoint.latitude.degrees
            lng = subpoint.longitude.degrees
            elevation = subpoint.elevation.km
            name = sat.name
            sat_obj  = Satellite(name ,lat , lng , elevation)
            if elevation>400: #ToDO : HINT : is it elevatino form sea level, if so ? how height this coordinate above sea level ?
                temp.append(sat_obj)
        print(len(temp))
        return temp

    def update_stas_poitions(self):
        print("Updating")
        self.sats = self.sats_list()
        self.sats_xy = self.stas_long_lats()

    def has_line_of_sight(self , pos1_xyz, pos2_xyz):
        # Vector between satellites
        vector = np.array(pos2_xyz) - np.array(pos1_xyz)
        midpoint = np.array(pos1_xyz) + 0.5 * vector

        # Distance of the midpoint from Earth's center
        distance_to_earth_center = np.linalg.norm(midpoint)

        # If the midpoint is outside Earth's radius, satellites have a line of sight
        return distance_to_earth_center > wgs84.polar_radius.km

    def load_sats_by_name(self):
        sats_raw = self.sats_raw
        by_name = {sat.name:sat for sat in sats_raw }
        return by_name

    #
    # def format_satlites_file_into_dict(self ):
    #     # load the stalites
    #     satellites = self.filemanger.load_satellites_files()
    #
    #     # Key = sat.model.satnum , [03-07] The unique satellite NORAD catalog number given in the TLE file. Ex: 2554
    #     # Value = sat
    #
    #     t = self.ts.now()
    #
    #     sats_dict = dict()
    #     start = time.time()
    #     for satellite in satellites:
    #         geometry = satellite.at(t)
    #         subpoint = geometry.subpoint()
    #
    #         if subpoint.elevation.km > 400:
    #             sat_santum = satellite.model.satnum
    #
    #             sats_dict[sat_santum] = Satellite(
    #                 sat_santum,
    #                 latitude= subpoint.latitude.degrees,
    #                 longitude= subpoint.longitude.degrees,
    #                 altitude=subpoint.elevation.km,
    #                 sat=satellite
    #             )
    #
    #     end = time.time()
    #     print("Execution Time inserting Sats to Dict= " , (end-start)   , "seconds")
    #
    #     # mydict  ={ sat.model.satnum : Satellite(sats)  sat.at(t).subpoint() for sat in sats }
    #     print(len(sats_dict))
    #
    #     return sats_dict

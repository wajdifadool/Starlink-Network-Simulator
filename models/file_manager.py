import os
import json
from skyfield.api import load
from skyfield.iokit import parse_tle_file

class FileManager:
    def __init__(self, directory: str = 'data'):
        self.directory = directory

    def load_satellites_file(self, file_name: str = '3le.tle'):
        """Load the 3le.tle file that contains the satellites data  """
        script_dir = os.path.dirname(self.directory)
        file_path = os.path.join(script_dir, self.directory, file_name)

        ts = load.timescale()

        with load.open(file_path) as f:
            satellites = list(parse_tle_file(f, ts))
            k = 12
        # TODO: Logger for Development  Enviormnet  and testing
        # print('Loaded file ', file_name, 'length=', len((satellites)))

        return satellites

    def load_ground_stations(self, file_name: str = 'locations_coordinates.json'):
        # Load station data from JSON file

        script_dir = os.path.dirname(self.directory)
        file_path = os.path.join(script_dir, self.directory, file_name)

        with open(file_path, "r") as file:
            station_data = json.load(file)
        # print('Loaded', len(station_data), 'Ground Stations')
        return station_data

    def save_file(self, file_name, str, data: dict):
        """save data into a file """
        pass

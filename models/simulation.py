from models.graph_utils import  GraphUtils
from  models.ground_control import  GroundControl
from skyfield.api import load
from datetime import timedelta
from  models.file_manager import  FileManager
from  models.satellite import  Satellite
import  re
import  pickle
from random import  shuffle
import models.utils as utils
from  models.user import  User
from models.graph_utils import  CAPACITY
class Simulation:

    def __init__(self, gc:GroundControl , users):
        self.gc = gc
        # self.users_list = users
        self.users = users
        self.users_length = len(self.users)
        self.res = []
        self.simulate_timestamps()


    def simulate_timestamps(self):
        # Initialize timescale
        ts = load.timescale()
        now = ts.now()

        # Generate timestamps with 10-minute intervals for 90 minutes
        interval_minutes = 10
        total_duration_minutes = 90
        time_stamps = [ts.now() + timedelta(minutes=i)
                       for i in range(0, total_duration_minutes , interval_minutes)]

        print(f"len of time tamps = {len(time_stamps)}")

        # create the max flow
        sats = []
        flows = []

        for m_time in time_stamps:
            # Create sats
            sat_i = self._create_my_satellites(m_time)

            # build max flow graph
            graph_utils = GraphUtils(ground_control= self.gc, ground_users=self.users, sats=sat_i )

            flow_sats = graph_utils.get_max_flow_satellites()
            flow_value = graph_utils.get_max_flow_value()

            current_flow_holder = {
                "time":m_time,
                "flow_sats": flow_sats,
                "flow_value_GB": flow_value ,
                "user_group_count" : self.users_length,
                "capacity" : {
                    "s2s" : CAPACITY.S2S.value ,
                    "s2g": CAPACITY.S2G.value,
                    "s2u": CAPACITY.S2U.value,
                }
            }

            self.res.append(current_flow_holder)



        globall = "global"
        usa = "USA"
        usa_ca_aus_eu = "usa_ca_aus_eu"


        file_name = f"max_flow_full_day_s2s_{CAPACITY.S2S.value}_{globall}_{self.users_length}"
        with open(file_name, 'wb') as file:
            pickle.dump(self.res, file)

    def _create_my_satellites(self , m_time ):
        fm = FileManager()
        file_data = fm.load_tle_file_into_list()

        temp = []
        for sat in file_data:
            geometry = sat.at(m_time)
            subpoint = geometry.subpoint()
            sat_elevation = subpoint.elevation.km

            if  600 > sat_elevation > 500  :
                sat_lat = subpoint.latitude.degrees
                sat_lng = subpoint.longitude.degrees

                sat_xyz = geometry.position.km
                # "Starlink-1008" will be now "1008", faster
                sat_name  = re.search(r"-(\d+)$",  sat.name).group(1)
                satellite = Satellite(sat_name, latitude=sat_lat, longitude=sat_lng, altitude=sat_elevation,
                                      sat_xyz=sat_xyz ,total_flow=None)
                temp.append(satellite)
        shuffle(temp)
        return temp


from models.ground_control import GroundControl
from visualization.satellite_tracker import SatelliteTracker
from PyQt5.QtWidgets import QApplication
import logging

from models.graph_utils import  GraphUtils
from models.simulation import  Simulation
from  visualization.flow_visual import FlowVisual

import models.utils as utils

def main():

    # init ground control !
    ground_control = GroundControl()

    # Create Users
    users1 = utils.generate_ground_users_1(5000) # ALL OVER EARTH
    users2 = utils.generate_ground_users_2(5000) # United States
    users3 = utils.generate_ground_users_3(5000) # Europe, USA, Canada, and Australia.


    # this is for creating the graph and the max flow
    simulation = Simulation(ground_control , users1 )

    # flow_visual = FlowVisual(ground_control)


    # """
    # Init app visualization
    # app = QApplication([])
    # tracker = SatelliteTracker(ground_control , users3)
    # tracker.show()
    # app.exec_()


    # init max_flow visual

if __name__ == "__main__":
    main()
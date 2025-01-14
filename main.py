from models.ground_control import GroundControl
from visualization.satellite_tracker import SatelliteTracker
from PyQt5.QtWidgets import QApplication

from models.graph_utils import  GraphUtils
from models.simulation import  Simulation
import models.utils as utils
import logging
import threading


def main():
    # Configure the logger
    # logging.basicConfig(
    #     level=logging.DEBUG,  # Set the minimum log level
    #     format='%(asctime)s - %(levelname)s - %(message)s'  # Format of the log message
    # )
    # # Supress matplotlib debug loging
    # logging.getLogger('matplotlib').setLevel(logging.ERROR)

    # Init ground Controls object
    ground_control = GroundControl()

    # generate users
    users = utils.generate_ground_users(10)

    # Init Graph utils
    graphs = GraphUtils(ground_control , users)


    # init simulations
    # simulation = Simulation(graphs)
    # simulation.run(None)

    # Init app visualization
    app = QApplication([])
    tracker = SatelliteTracker(ground_control , users=users)
    tracker.show()
    app.exec_()







if __name__ == "__main__":
    main()
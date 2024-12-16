from models.ground_control import GroundControl
from visualization.satellite_tracker import SatelliteTracker
from PyQt5.QtWidgets import QApplication


def main():

    ground_control = GroundControl()

    app = QApplication([])
    tracker = SatelliteTracker(ground_control)
    tracker.show()
    app.exec_()


if __name__ == "__main__":
    main()
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from matplotlib.widgets import RectangleSelector
from skyfield.iokit import parse_tle_file
from skyfield.api import load

from  models.ground_control import GroundControl
from models.satellite import Satellite


class SatelliteTracker(QMainWindow):
    def __init__(self, ground_control:GroundControl):
        super().__init__()
        self.satellite_annotations = []  # Store annotations for satellites

        self.update_interval:int = (10*(10**3))
        self.gc =  ground_control
        self.setWindowTitle("Real-Time Satellite Tracker")

        self.showMaximized()

        # Set up the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create Matplotlib Figure
        self.fig = Figure()

        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        # Adjust figure layout to remove margins
        self.fig.tight_layout(pad=0)  # Automatically fit elements with no extra padding
        self.fig.subplots_adjust(left=0, right=1, top=0.95, bottom=0)  # Fill the entire canvas


        # Initialize plot
        self.ax = self.fig.add_subplot(111, projection=ccrs.PlateCarree())
        self.ax.stock_img()
        self.ax.add_feature(cfeature.BORDERS, linestyle=":")
        self.ax.add_feature(cfeature.COASTLINE)
        self.ax.set_title("Real-Time Starlink Satellite Tracker" , pad=10)


        # Initial plotting
        self.satellite_scatter = None
        self.plot_satellites()
        self.plot_stations()

        # Set up timer for updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_satellite_positions)
        self.timer.start(self.update_interval)  # Update every 20 seconds

    def plot_satellites(self):
        """Plot satellites on the map."""
        # print("calling  updat e satlites ")

        # Remove old annotations if any
        for annotation in self.satellite_annotations:
            annotation.remove()
        self.satellite_annotations.clear()


        lats_longs = self.gc.fetch_lat_long()
        latitudes = lats_longs[0]
        longitudes = lats_longs[1]


        # Plot satellites as red points
        self.satellite_scatter = self.ax.scatter(
            longitudes,
            latitudes,
            color='red',
            s=3,
            marker="s",
            transform=ccrs.PlateCarree(),
        )

        # Annotate each satellite with its name
        for name, (lat, lon, _) in self.gc.dict_name_lat_lng.items():
            annotation = self.ax.annotate(
                name,
                xy=(lon, lat),
                xytext=(3, 3),  # Offset the text slightly
                textcoords='offset points',
                fontsize=6,
                color='black',
                transform=ccrs.PlateCarree(),
            )
            self.satellite_annotations.append(annotation)
        self.canvas.draw()
    #
    def plot_stations(self):
        gs_tuples = self.gc.ground_stations_long_lats
        latitudes = gs_tuples[0]
        longitudes = gs_tuples[1]

        # Plot stations as blue squares
        self.ax.scatter(
            longitudes,
            latitudes,
            color="blue",
            s=5,
            transform=ccrs.PlateCarree(),
            marker="s",
        )
        self.ax.legend()


    def update_satellite_positions(self):
        # print("calling update UI ")
        if self.satellite_scatter:
            self.satellite_scatter.remove()

        self.gc.refresh_dict_lat_lng()
        self.plot_satellites()


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
        self.update_interval:int = 5000
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

        # TODO: DO we need this ?
        # # Initialize rectangle selector
        # self.rectangle_selector = RectangleSelector(
        #     self.ax,
        #     self.on_select,
        #     interactive=True,
        #     button=[1],  # Left mouse button
        #     useblit=True  # Optimized rendering
        # )

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
        sats_tuple = self.gc.sats_xy
        latitudes = sats_tuple[0]
        longitudes = sats_tuple[1]

        # Plot satellites as red points
        self.satellite_scatter = self.ax.scatter(
            longitudes,
            latitudes,
            color='red',
            s=3,
            marker="s",
            transform=ccrs.PlateCarree(),
        )
        self.canvas.draw()

    def plot_stations(self):
        gs_tuples = self.gc.gs_xy
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

        self.satellite_scatter.remove()
        self.gc.update_stas_poitions()
        self.plot_satellites()

    # TODO: do we need this ?
    # def on_select(self, eclick, erelease):
    #     """Handle rectangle selection."""
    #     # Convert rectangle bounds to map coordinates
    #     lon_min, lon_max = sorted([eclick.xdata, erelease.xdata])
    #     lat_min, lat_max = sorted([eclick.ydata, erelease.ydata])
    #
    #     # Ensure valid coordinates
    #     if None in (lon_min, lon_max, lat_min, lat_max):
    #         return
    #
    #     # Select satellites within the rectangle
    #     selected_satellites = []
    #
    #     for sat in self.satellite_data:
    #         if lon_min <= sat["longitude"] <= lon_max and lat_min <= sat["latitude"] <= lat_max:
    #             selected_satellites.append(sat)
    #
    #     # Select stations within the rectangle
    #     selected_stations = []
    #     for name, data in self.station_data.items():
    #         if lon_min <= data["Longitude"] <= lon_max and lat_min <= data["Latitude"] <= lat_max:
    #             selected_stations.append({"name": name, "latitude": data["Latitude"], "longitude": data["Longitude"]})
    #
    #     # Print selected satellites
    #     if selected_satellites:
    #         print(f"Found {len(selected_satellites)} Satellites:")
    #         for sat in selected_satellites:
    #             print(
    #                 f"  Name: {sat['name']}, Latitude: {sat['latitude']:.2f}, Longitude: {sat['longitude']:.2f}, Elevation: {sat['elevation_km']:.2f} km"
    #             )
    #     else:
    #         print("No satellites found in the selected region.")
    #
    #     # Print selected stations
    #     if selected_stations:
    #         print(f"Found {len(selected_stations)} Stations:")
    #         for station in selected_stations:
    #             print(
    #                 f"  Name: {station['name']}, Latitude: {station['latitude']:.2f}, Longitude: {station['longitude']:.2f}"
    #             )
    #     else:
    #         print("No stations found in the selected region.")

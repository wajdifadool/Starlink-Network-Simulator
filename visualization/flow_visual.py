import os
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from models.graph_utils import GraphUtils
from  models.satellite import  Satellite
from  models.ground_control import  GroundControl
import  pickle

class FlowVisual():
    def __init__(self , ground_control:GroundControl):
        # Load the data for max flow

        f1 = "max_flow_full_day_s2s_20_global_5000"
        f2="max_flow_full_day_s2s_20_USA_5000"
        f3="max_flow_full_day_s2s_20_usa_ca_aus_eu_5000"

        f4 = "max_flow_full_day_s2s_200_global_5000"
        f5 = "max_flow_full_day_s2s_200_USA_5000"
        f6 = "max_flow_full_day_s2s_200_usa_ca_aus_eu_5000"

        self.gc = ground_control
        with open(f1, 'rb') as file:
            m_flows =  pickle.load(file)


        self.max_flow_nodes = m_flows[2]["flow_sats"]
        mmax_flow  = m_flows[0]["flow_value_GB"]
        print(f"max_FLOW_GB{mmax_flow}")

        self.plot_flow_on_map_with_analysis()

    def plot_flow_on_map_with_analysis(self):
        """
        Plot satellites and flow values on a static map using real positions.
        Analyze the flow distribution and print statistics.
        """

        flows = self.max_flow_nodes
        # # Analyze flow data
        min_flow = flows[-1].total_flow

        max_flow = flows[0].total_flow
        mid_flow = (min_flow + max_flow) / 2

        # count_min = sum(1 for v in flows.values() if v == min_flow)
        # count_max = sum(1 for v in flows.values() if v == max_flow)
        # count_mid = sum(1 for v in flows.values() if v > min_flow and v < max_flow)
        # count_below_mid = sum(1 for v in flows.values() if v <= mid_flow)
        # count_above_mid = sum(1 for v in flows.values() if v > mid_flow)


        # # Print analysis
        # print("Flow Analysis:")
        # print(f"Total satellites: {len(flows)}")
        # print(f"Satellites with minimum flow ({min_flow}): {count_min}")
        # print(f"Satellites with maximum flow ({max_flow}): {count_max}")
        # print(f"Satellites with flow between min and max: {count_mid}")
        # print(f"Satellites with flow <= mid ({mid_flow}): {count_below_mid}")
        # print(f"Satellites with flow > mid ({mid_flow}): {count_above_mid}")

        # Determine flow value range for normalization
        norm = Normalize(vmin=min_flow, vmax=max_flow)
        cmap = cm.get_cmap('RdYlGn_r')  # Reverse the colormap to make red maximum and green minimum

        # Set up the map with maximized figure size
        # fig = plt.figure(figsize=(20, 12))  # Larger figure size for full screen
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_global()  # Ensure the map is global
        ax.stock_img()
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.add_feature(cfeature.COASTLINE)

        # Plot satellites on the map
        for sat in flows :
            lat, lon = sat.latitude , sat.longitude
            color = cmap(norm(sat.total_flow))  # Map flow value to color
            ax.scatter(
                lon,
                lat,
                color=color,
                s=5,  # Smaller size for the points
                transform=ccrs.PlateCarree(),
                marker="o",
            )

        # Add a compact colorbar inside the map
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])  # Required for matplotlib colorbar
        cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.05, aspect=50, shrink=0.5)  # Compact colorbar
        cbar.set_label('Flow Value', fontsize=10)  # Smaller font size for the label
        cbar.ax.tick_params(labelsize=8)  # Smaller font size for tick labels

        name = 2
        # plt.title(f'Satellite Flow Visualization - {os.path.basename(pickle_file)}', fontsize=16, pad=20)
        # plt.savefig(f"{name}.png", dpi=300, bbox_inches="tight")
        plt.tight_layout(rect=[0, 0, 1, 0.95])  # Maximize the map usage
        #

        # plt.tght_layout(pad=0)  # Automatically fit elements with no extra padding
        #         # plt.subplots_adjust(left=0, right=1, top=0.95, bottom=0)  # Fill the entire canvasi



        # plot ground stations
        my_gc = self.gc.my_ground_stations

        lats = [gs.latitude for gs in my_gc]
        longs = [gs.longitude for gs in my_gc]

        # Plot stations as blue squares
        ax.scatter(
            longs,
            lats,
            color="blue",
            s=2,
            transform=ccrs.PlateCarree(),
            marker="s",
        )

        plt.show()





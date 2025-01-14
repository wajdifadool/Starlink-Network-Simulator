from skyfield.api import wgs84, load
import networkx as nx
import  numpy as np
import time
import matplotlib.pyplot as plt
import random
import pylab
import logging
from enum import Enum
import  pickle
from models.satellite import Satellite
from models.file_manager import FileManager

# Graph utils constants
class CAPACITY(Enum):
    S2S = 2000  # satellite_to_satellite
    S2G = 800000 # satellite_to_ground
    S2U =  200 #  satellite_to_user
class Graph_nodes(Enum):
    Satellite = 1
    Ground_station = 2
    User = 3

INFINITY = float('inf')
ROOT_GC = "root_gc"  # this is our sink
ROOT_USER = 'root_user' # this is the Source


class GraphUtils :
    def __init__(self, ground_control , ground_users):
        print("GraphUtils invoked")
        self.ground_control  = ground_control
        self.satellites_dict: dict = ground_control.sats_dict_object_raw
        self.satellites_dict_lats_longs: dict = ground_control.dict_name_lat_lng # Holds <name>: <lat , lng , xyz>

        self.ground_stations_raw = self.ground_control.ground_stations_raw
        self.network = nx.DiGraph()
        self.users = ground_users


        load_graph_from_file = True

        if load_graph_from_file :
            self.network = pickle.load(open('graph.pickle', 'rb'))
        else:
            self.build_connectivity_graph_for_max_flow()
            # save graph object to file
            pickle.dump(self.network, open('graph.pickle', 'wb'))


        print(f" self.network = {self.network}")

        load_max_flow_from_file= True

        if load_max_flow_from_file:
            self.flow_obj = pickle.load(open('max_flow_obj.pickle', 'rb'))
            print("loaded flow_obj from file")
            flow_dict = self.flow_obj["flow_dict"]

            sorted_nodes = self.get_most_used_nodes(flow_dict)

        else:
            max_flow_value, flow_dict = self.simulate_max_flow(ROOT_GC, ROOT_USER)
            flow_obj = {
                "max_flow_value": max_flow_value,
                "flow_dict": flow_dict
            }

            pickle.dump(flow_obj, open('max_flow_obj.pickle', 'wb'))
            print("saved flow_obj into file")


        # nx.draw(G, with_labels=True)
        # plt.show()


        # median = self.calculate_avg_of_medians()
        # print(median)


    def build_connectivity_graph_for_max_flow(self):
        """Build a graph of satellite connectivity based on line of sight

        each Node splits into 2 node, node_in, node_out and the capicity is now betwwen in and out"""

        print("build_connectivity_graph() --> started")
        start = time.time()
        self.connect_satellites()
        self.connect_ground_stations()
        self.connect_users() # todo: this is scinario

        end = time.time()
        print("build_connectivity_graph() --> Completed ")
        print(f"time took {end - start} for{self.network}")


    # GRAPHS methods
    def connect_satellites(self):

        # add the  satlites as nodes
        for sat_name in self.satellites_dict.keys():
            self.network.add_node(f"{sat_name}_in", type=Graph_nodes.Satellite)
            self.network.add_node(f"{sat_name}_out", type=Graph_nodes.Satellite)
            self.network.add_edge(f"{sat_name}_in", f"{sat_name}_out", capacity=CAPACITY.S2S.value)

        # Add edges between satellites based on LOS
        for sat1_name, sat1 in self.satellites_dict_lats_longs.items():
            for sat2_name, sat2 in self.satellites_dict_lats_longs.items():
                if sat1_name != sat2_name:
                    sat1_xyz = sat1[2]
                    sat2_xyz = sat2[2]

                    # TODO: ennhance calulcation if posiple do some memoiztion if sta1_sat2 line of
                    #  sight calculted before , dont calucalte again
                    if self.has_line_of_sight_sat_to_sat(sat1_xyz, sat2_xyz):
                        self.network.add_edge(f"{sat1_name}_out", f"{sat2_name}_in",  capacity=INFINITY)
                        self.network.add_edge(f"{sat2_name}_out", f"{sat1_name}_in", capacity=INFINITY)

    def connect_ground_stations(self):
        # Adding the Ground Stations Nodes
        m_gc = self.ground_stations_raw
        # Add main Ground station Node and Edges
        self.network.add_node(ROOT_GC, type=Graph_nodes.Ground_station)

        # Example:   for the key, value loop
        # gc_name: Molokai, HI
        # gc_coords : {'Latitude': 21.1127, 'Longitude': -157.06323}
        for gc_name, gc_coords in m_gc.items():
            lat = gc_coords['Latitude']
            lon = gc_coords['Longitude']
            self.network.add_node(gc_name, type=Graph_nodes.Ground_station, lat=lat, lon=lon)
            self.network.add_edge(ROOT_GC, gc_name, capacity=CAPACITY.S2G.value)


        # Adding the Ground station->satlite Edges
        for station_name , station in m_gc.items():
            # TODO: calculate xyz pre run and add them to json file
            # Convert ground station lat/lon to XYZ using WGS84
            ground_position = wgs84.latlon(station['Latitude'], station['Longitude'])
            ground_xyz = ground_position.itrs_xyz.km  # Convert from AU to km directly

            for sat_name, sat in self.satellites_dict_lats_longs.items():
                # Satellite position in XYZ (already in Cartesian coordinates)
                sat_xyz = np.array(sat[2])
                has_line_of_sight = self.has_line_of_sight_sat_to_ground_station(sat_xyz,ground_xyz )
                if has_line_of_sight :
                    self.network.add_edge(station_name, f"{sat_name}_in", capacity=INFINITY)


        k= self.network

        j = 9

    def connect_users(self):
        # adding the users
        k=4
        for user in self.users:
            user_xyz = user.xyz
            for sat_name, sat in self.satellites_dict_lats_longs.items():
                sat_xyz = np.array(sat[2])  # Cartesian coordinates
                has_line_of_sight = self.has_line_of_sight_sat_to_ground_station(sat_xyz, user_xyz,
                                                                                 default_distance=1750)
                if has_line_of_sight:
                    self.network.add_edge(f"{sat_name}_out", user.user_id, capacity=INFINITY)
                    break  # conect only once
        print("Users conected ")

        # ADD the Root User
        self.network.add_node(ROOT_USER, type=Graph_nodes.User)

        for user in self.users:
            self.network.add_edge(user.user_id, ROOT_USER, capacity=CAPACITY.S2U.value * k)

    def simulate_max_flow(self, source, sink):
        """
        Simulate maximum flow on the graph (self.network).

        Parameters:
        - source: The source node (e.g., ROOT_GC).
        - sink: The sink node (e.g., ROOT_USER).

        Returns:
        - max_flow_value: The value of the maximum flow.
        - flow_dict: The flow distribution in the network.
        """
        # Use the Edmonds-Karp algorithm to compute max flow
        max_flow_value, flow_dict = nx.maximum_flow(self.network, source, sink, capacity='capacity' )
        return max_flow_value, flow_dict

    def has_line_of_sight_sat_to_sat(self , pos1_xyz, pos2_xyz):
        """
        # check LOS (line of sight) between two satellites
        :param pos1_xyz:
        :param pos2_xyz:
        :return: True If the midpoint is outside Earth's radius,
         meaning satellites have a line of sight, False Otherwise
        """
        # Vector between satellites
        vector = np.array(pos2_xyz) - np.array(pos1_xyz)
        midpoint = np.array(pos1_xyz) + 0.5 * vector

        # Distance of the midpoint from Earth's center
        distance_to_earth_center = np.linalg.norm(midpoint)

        # If the midpoint is outside Earth's radius, satellites have a line of sight
        return distance_to_earth_center > wgs84.polar_radius.km

    def has_line_of_sight_sat_to_ground_station(self , sat_xyz, ground_xyz , default_distance = 2000):
        """
        # check LOS (line of sight) between a satellite and ground station
        :param pos1_xyz:
        :param pos2_xyz:
        :return: True If the Euclidean distance is less the 2000 between the two objects
        """
        # Calculate Euclidean distance
        distance = np.linalg.norm(sat_xyz - ground_xyz)
        # 1760 for user
        return distance < default_distance

    def shortest_path(self, start, end) -> list:
        """Find the shortest path between two satellites."""
        return  nx.shortest_path(self.network , start , end )

    def calculate_avg_of_medians(self):
        """
        Calculate the average of the median distances between satellites that can see each other.

        :param satellites: A dictionary where keys are satellite names and values are XYZ coordinates (e.g., {'sat1': [x, y, z], ...}).
        :return: The average of the median distances.
        only used to calculate determinate the user conenct to satlite distance
        """
        medians = []

        for sat1_name, sat1 in self.satellites_dict_lats_longs.items():
            distances = []
            for sat2_name, sat2 in self.satellites_dict_lats_longs.items():
                if sat1_name != sat2_name:
                    sat1_xyz = sat1[2]
                    sat2_xyz = sat2[2]
                    if self.has_line_of_sight_sat_to_sat(sat1_xyz, sat2_xyz):
                        # Calculate Euclidean distance
                        distance = np.linalg.norm(np.array(sat1_xyz) - np.array(sat2_xyz))
                        distances.append(distance)
            if distances:
                # Calculate the median distance for the current satellite
                median_distance = np.average(distances)
                medians.append(median_distance)

        if medians:
            # Calculate the average of all median distances
            avg_of_medians = np.average(medians)
            return avg_of_medians
        # returnd 3515 for file 3tle.full


        return 0  # If there are no medians, return 0

    def get_most_used_nodes(self , flow_dict):
        """Get nodes that are most involved in the flow."""
        node_flow = {}
        for u, flows in flow_dict.items():
            total_flow = sum(flows.values())
            node_flow[u] = total_flow

        # Sort nodes by total flow
        sorted_nodes = sorted(node_flow.items(), key=lambda x: x[1], reverse=True)
        return sorted_nodes


## Static methods
def print_graph_edges(network:nx.DiGraph):
    logging.debug("Printing Graph Network ... ")
    for edge in network.edges(data=False):
        print(edge)

def print_graph_nodes(network: nx.DiGraph):
    # print(self.network)
    logging.debug("Graph Network ( Only Nodes )  ... ")
    for node in network.nodes(data=True):
        print(node)

def draw_graph(network: nx.DiGraph) :
    nx.draw(network , with_labels=True)
    plt.show()
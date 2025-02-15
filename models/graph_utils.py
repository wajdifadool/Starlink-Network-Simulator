from skyfield.api import wgs84
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
from  models.ground_control import  GroundControl
import math
import numpy as np
from skyfield.api import wgs84
from itertools import combinations
from random import  shuffle

EARTH_RADIUS = wgs84.polar_radius.km
# Graph utils constants
class CAPACITY(Enum):
    S2S = 200//10   # satellite_to_satellite  # 200GB
    S2G = 80      # satellite_to_ground       # 80GB
    S2U = 0.2     # satellite_to_user      # 0.2GB = 200MB


class Graph_nodes(Enum):
    Satellite =      1
    Ground_station = 2
    User =           3

INFINITY = float('inf')
ROOT_GC = "root_gc"     # this is our sink
ROOT_USER = 'root_user' # this is the Source
default_distance = 2000

class GraphUtils :
    def __init__(self, ground_control:GroundControl , ground_users , sats):
        print("GraphUtils():: __INIT__ invoked")

        self.ground_control  = ground_control
        self.satellites =  sats
        self.ground_stations = self.ground_control.my_ground_stations
        self.users = ground_users

        self.network:nx.DiGraph = nx.DiGraph()
        self.build_connectivity_graph_for_max_flow()

        max_flow, flow_dict  = self.simulate_max_flow(ROOT_GC, ROOT_USER)
        self.network_max_flow = max_flow
        self.save_flow_most_used_node(flow_dict)
        # 50 * 2 = 100GB,
        print(f"GraphUtils:: max flow is  ={max_flow} GB")

    def build_connectivity_graph_for_max_flow(self):
        """
         Build a graph of satellite connectivity based on line of sight
         each Node splits into 2 node, node_in, node_out and the
         capicity is now betwwen in and out
        """

        print("build_connectivity_graph() --> started")
        start = time.time()
        self.connect_satellites()
        self.connect_ground_stations()
        self.connect_users(self.users)
        end = time.time()

        print("build_connectivity_graph() --> Completed ")
        print(f"time took {end - start} for{self.network}")

    def connect_satellites(self):
        # add the sats as nodes
        for sat in self.satellites:
            sat_name = sat.satellite_id
            self.network.add_node(f"{sat_name}_in", type=Graph_nodes.Satellite , lat=sat.latitude , lon=sat.longitude)
            self.network.add_node(f"{sat_name}_out", type=Graph_nodes.Satellite)
            self.network.add_edge(f"{sat_name}_in", f"{sat_name}_out", capacity=CAPACITY.S2S.value)

        # Add edges between satellites based on LOS
        for sat1 , sat2  in combinations(self.satellites ,2):
            sat1_xyz = sat1.sat_xyz
            sat2_xyz = sat2.sat_xyz
            sat1_name = sat1.satellite_id
            sat2_name = sat2.satellite_id
            if self.has_los_sat_sat(sat1_xyz, sat2_xyz):
                self.network.add_edge(f"{sat1_name}_out", f"{sat2_name}_in", capacity=INFINITY )
                self.network.add_edge(f"{sat2_name}_out", f"{sat1_name}_in", capacity=INFINITY)

    def connect_ground_stations(self):
        # Adding the Ground Stations Nodes
        ground_stations = self.ground_stations
        satellites =  self.satellites
        # Add main Ground station Node and Edges
        self.network.add_node(ROOT_GC, type=Graph_nodes.Ground_station)

        for gc in ground_stations:
            self.network.add_node(gc.station_id, type=Graph_nodes.Ground_station)
            self.network.add_edge(ROOT_GC, gc.station_id, capacity=CAPACITY.S2G.value)

        for gc in ground_stations:
            ground_xyz = gc.xyz
            gc_name = gc.station_id
            for sat in satellites:
                if self.has_los_earth_sat(sat.sat_xyz, ground_xyz):
                    self.network.add_edge(gc_name, f"{sat.satellite_id}_in", capacity=INFINITY)

    def connect_users(self, users):
        m_set= set()
        connected_sats = {}
        # adding the users , each group is of k users
        group_size = 50
        for user in users:
            user_xyz = user.xyz

            shuffle(self.satellites)
            shuffle(self.satellites)

            for sat in self.satellites:
                # TODO: conect to the closest , maybe we dont need that ?
                # all los -> select the closest
                # Time O(n  * m )
                if self.has_los_earth_sat(sat.sat_xyz, user_xyz):
                    self.network.add_edge(f"{sat.satellite_id}_out", user.user_id, capacity=INFINITY)

                    # this is for see how many conected user in each
                    # sat.connected_users+=1 # update the number of
                    # m_set.add(sat.satellite_id)
                    #
                    # if  sat.satellite_id in connected_sats :
                    #     connected_sats[sat.satellite_id] = connected_sats[sat.satellite_id]+1
                    # else :
                    #     connected_sats[sat.satellite_id] = 1

                    break  # Connect only once

        # print(f"all conected satts are {m_set} , len= {len(m_set)}")
        # connected_sats_sorted = sorted(connected_sats.values())
        #
        # # '''
        # # Plot the distribution
        # plt.figure(figsize=(8, 5))
        # plt.plot(connected_sats_sorted, marker='o', linestyle='-', color='b', label="User Distribution")
        #
        # # Labels and title
        # plt.xlabel("Satellite Index (Sorted)")
        # plt.ylabel("Number of Users Connected")
        # plt.title("Distribution of Users Across Satellites")
        # plt.legend()
        # plt.grid(True)
        # # Display total user count on the graph
        # plt.text(0.5, 0.9, f"Total groups of : {sum(connected_sats.values())}",
        #          transform=plt.gca().transAxes, fontsize=12,
        #          bbox=dict(facecolor='white', alpha=0.8))
        # # Show the plot
        # plt.show()
        # for k , v in connected_sats.items() :
        #     print(f"{k} : {v}")
        # '''


        # Extract values (user counts)
        # user_counts = list(connected_sats.values())
        #
        # # Calculate total users
        # total_users = sum(user_counts)
        #
        # # Create histogram
        # plt.figure(figsize=(8, 5))
        # plt.hist(user_counts, bins=5, edgecolor='black', alpha=0.7, color='b')
        #
        # # Labels and title
        # plt.xlabel("Number of Users Connected")
        # plt.ylabel("Frequency of Satellites")
        # plt.title("Histogram of User Connections per Satellite")
        #
        # # Display total user count
        # plt.text(0.6, 0.9, f"Total Users: {sum(user_counts)}",
        #          transform=plt.gca().transAxes, fontsize=12,
        #          bbox=dict(facecolor='white', alpha=0.8))
        #
        # plt.grid(axis='y', linestyle='--', alpha=0.7)
        #
        # # Show the plot
        # plt.show()

        # ADD the Root User
        self.network.add_node(ROOT_USER, type=Graph_nodes.User)
        for user in users:
            capacity = CAPACITY.S2U.value * group_size

            self.network.add_edge(user.user_id, ROOT_USER, capacity = capacity)
            # 50 * 2 = 100GB * 5000 = 500,000


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
        max_flow_value, flow_dict = nx.maximum_flow(self.network, source, sink, capacity='capacity' ,
                                                    flow_func=nx.algorithms.flow.shortest_augmenting_path  )
        return max_flow_value, flow_dict

    def has_los_sat_sat(self, pos1_xyz, pos2_xyz):
        """
        Check line of sight for multiple satellite pairs using batch processing.
        :param pos1_xyz: Array of XYZ positions for satellite 1 (N x 3).
        :param pos2_xyz: Array of XYZ positions for satellite 2 (N x 3).
        :return: Boolean array indicating line of sight for each pair.
        """
        # Calculate vectors and midpoints
        vectors = pos2_xyz - pos1_xyz
        midpoints = pos1_xyz + 0.5 * vectors

        # # Calculate distances from Earth's center
        distances = np.linalg.norm(midpoints)

        # Check if distances are greater than Earth's radius
        return distances > EARTH_RADIUS

    def has_los_earth_sat(self , sat_xyz, ground_xyz ):
        """
        # check LOS (line of sight) between a satellite and ground station
        :param pos1_xyz:
        :param pos2_xyz:
        :return: True If the Euclidean distance is less the 2000 between the two objects
        """
        # Calculate Euclidean distance
        distance = np.linalg.norm(sat_xyz - ground_xyz)

        return distance < default_distance

    def shortest_path(self, start, end) -> list:
        """Find the shortest path between two satellites."""
        return  nx.shortest_path(self.network , start , end )

    def save_flow_most_used_node(self , flow_dict):
        """Get nodes that are most involved in the flow.
        only the _in nodes """
        node_flow_list = []
        m_net = self.network

        for u, flows in flow_dict.items():
            if u.endswith("_in"):
                lat = m_net.nodes._nodes[u]["lat"]
                lon = m_net.nodes._nodes[u]["lon"]

                total_flow = sum(flows.values())
                sat = Satellite(satellite_id=u ,latitude=lat , longitude=lon,altitude=None ,sat_xyz=None,
                                total_flow= total_flow)
                node_flow_list.append(sat)

        # Sort nodes by total flow
        sorted_nodes = sorted(node_flow_list, key=lambda sat: sat.total_flow, reverse=True)

        # l = 12
        # print(sorted_nodes[0].total_flow)
        # print(sorted_nodes[-1].total_flow)


        self.node_flows = sorted_nodes

    def get_max_flow_satellites(self):
        return self.node_flows

    def get_max_flow_value(self):
        return self.network_max_flow

    def get_max_flow_nodes(self)->dict:
        return self.node_flows




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
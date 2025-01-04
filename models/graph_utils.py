from skyfield.api import wgs84, load
import networkx as nx
from models.satellite import Satellite
import  numpy as np
from models.file_manager import FileManager
import time

import logging

# TODO: change DEFAULT_CAPACITY ( search for more accurate values ) , MOVE TO RUNTIME VALUES FILE
DEFAULT_CAPACITY = {
            'satellite_to_satellite': 200,  # Mbps
            'satellite_to_ground': 50,  # Mbps
            'ground_to_user': 20  # Mbps
}

class GraphUtils:
    def __init__(self, ground_control):
        self.ground_control  = ground_control
        self.satellites_dict: dict = ground_control.sats_dict_object_raw
        self.satellites_dict_lats_longs: dict = ground_control.dict_name_lat_lng # Holds <name>: <lat , lng , xyz>

        self.ground_stations_raw = self.ground_control.ground_stations_raw

        self.network = nx.DiGraph()
        self.build_connectivity_graph()


    def build_connectivity_graph(self):
        """Build a graph of satellite connectivity based on line of sight."""

        logging.debug("build_connectivity_graph() --> started")
        logging.debug("build_connectivity_graph() --> Adding Nodes")

        # Add satellites names as nodes
        for sat_name in  self.satellites_dict.keys():
            self.network.add_node(sat_name, type='satellite')

        logging.debug("build_connectivity_graph() --> Adding Edges ")

        # TODO: use  memoization , example below,
        """
        # calcualte the run time  before adding this  
        pairs = [] 
        checked_pairs = set()
        if (sat1_name, sat2_name) not in checked_pairs and (sat2_name, sat1_name) not in checked_pairs:
            if self.has_line_of_sight_sat_to_sat(sat1_xyz, sat2_xyz):
                self.network.add_edge(sat1_name, sat2_name, capacity=DEFAULT_CAPACITY['satellite_to_satellite'])
            checked_pairs.add((sat1_name, sat2_name))
        """

        # Add edges between satellites based on LOS
        for sat1_name, sat1 in self.satellites_dict_lats_longs.items():
            for sat2_name, sat2 in self.satellites_dict_lats_longs.items():
                if sat1_name != sat2_name:
                    sat1_xyz = sat1[2]
                    sat2_xyz = sat2[2]
                    # TODO:: DO some memoization so we dont check checked pairs in different order twice
                    #  Example the pair  [sat2212 , sat:4432 ] is equal to pair [sat:4432 , sat2212]
                    #  so instead of checking it twice we could check first if the pairs in there,
                    #  if so don't calculate line of sight , aso we can use memoiztoin
                    #  inside  has_line_of__sight function it self , insted of doing the vector calculation each time
                    if self.has_line_of_sight_sat_to_sat(sat1_xyz , sat2_xyz):
                        self.network.add_edge(sat1_name, sat2_name, capacity=DEFAULT_CAPACITY['satellite_to_satellite'])


        # Adding the Ground Stations Nodes
        m_gc = self.ground_stations_raw
        # Example:   for the key, value loop
        # gc_name: Molokai, HI
        # gc_coords : {'Latitude': 21.1127, 'Longitude': -157.06323}
        for gc_name  , gc_coords in m_gc.items():
            lat = gc_coords['Latitude']
            lon = gc_coords['Longitude']
            self.network.add_node(gc_name, type='ground_station', lat=lat ,lon= lon)

         # Adding the Ground station Edges
        for station_name , station in m_gc.items():
            # Convert ground station lat/lon to XYZ using WGS84
            ground_position = wgs84.latlon(station['Latitude'], station['Longitude'])
            ground_xyz = ground_position.itrs_xyz.km  # Convert from AU to km directly

            for sat_name, sat in self.satellites_dict_lats_longs.items():
                # Satellite position in XYZ (already in Cartesian coordinates)
                sat_xyz = np.array(sat[2])
                has_line_of_sight = self.has_line_of_sight_sat_to_ground_station(sat_xyz,ground_xyz )
                if has_line_of_sight :
                    self.network.add_edge(station_name, sat_name, capacity=DEFAULT_CAPACITY['satellite_to_ground'])

        logging.debug("build_connectivity_graph() --> Completed ")
        logging.debug(self.network)


        # TEST Example:
        station_name1 = "Angola, Indiana"
        sat_name1 = "STARLINK-1142"
        sat_name2 = "STARLINK-1143"
        # print(self.network.nodes)
        if sat_name1 in  self.network.nodes :
            print("sat is there")
        if station_name1 in  self.network.nodes :
            print("station is there")
        self.is_path_exist(station_name1, sat_name1)

    def shortest_path(self, start: Satellite, end: Satellite) -> list:
        """Find the shortest path between two satellites."""
        pass

    def is_path_exist(self, source_node_name, sink_node_name):
        """
        Find if path exisets the shortest path between two satellites.

        :param source_node_name: Satellite, ground_station or user.
        :param sink_node_name: Satellite, ground_station or user.
        :return: true or false
        """
        k = nx.has_path(self.network, source_node_name,  sink_node_name )
        if k:
            print("path is founnd ")
            print(k)
        else:
            print("path is not found ")


    def scenario_number_1(self):
        """What scenario goes here ?"""
        # random  locations for 2  user with distance longer than 4000
        # random  locations for 2  users  beside each other ( same lat and long)
        # distribute users across the world uniformly !! how to do ?
        # all users in highly dense urban city
        # and more ...

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

    def has_line_of_sight_sat_to_ground_station(self , sat_xyz, ground_xyz):
        """
        # check LOS (line of sight) between a satellite and ground station
        :param pos1_xyz:
        :param pos2_xyz:
        :return: True If the Euclidean distance is less the 2000 between the two objects
        """
        # Calculate Euclidean distance
        distance = np.linalg.norm(sat_xyz - ground_xyz)
        # TODO : what is the distance here ?
        return distance < 2000

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

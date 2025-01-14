from models.graph_utils import  GraphUtils
class Simulation:
    def __init__(self,graphUtils:GraphUtils):
        self.graphUtils = graphUtils

    def run(self, scenario: dict):
        """Run the simulation for a specific scenario."""
        # find path of sight

        # sat1= "STARLINK-1240"
        # sat2 = "STARLINK-1201"

        sat1= "STARLINK-1308"
        sat2 = "STARLINK-1262"


        if self.graphUtils.is_path_exist(sat1,sat2):
            l = self.graphUtils.shortest_path(sat1  , sat2)

            print(f"path from {sat1}->{sat2}=={l}")
        else:
            print(f"no path from {sat1}->{sat2}")


    def scenario_number_1(self):
        """What scenario goes here ?"""
        # random  locations for 2  user with distance longer than 4000
        # random  locations for 2  users  beside each other ( same lat and long)
        # distribute users across the world uniformly !! how to do ?
        # all users in highly dense urban city
        # and more ...

    def update(self, delta_time: float):
        """Update the positions of satellites and state of the simulation."""
        pass
    def stop(self ):
        """Stop the simulation for a specific scenario."""
        pass



from models.world_map import  WorldMap
class Simulation:
    def __init__(self, satellites: list , ground_stations:list, users: list, world_map, WorldMap ):
        self.satellites = satellites
        self.ground_stations = ground_stations
        self.users = users
        self.world_map = world_map

    def run(self, scenario: dict):
        """Run the simulation for a specific scenario."""
        pass

    def update(self, delta_time: float):
        """Update the positions of satellites and state of the simulation."""
        pass
    def stop(self ):
        """Stop the simulation for a specific scenario."""
        pass



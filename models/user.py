class User:
    def __init__(self , user_id :int , location:tuple, bandwidth_requirements:float ):
        self.user_id = user_id
        self.location = location
        self.bandwidth_requirements = bandwidth_requirements

    def request_service(self, simulation: "Simulation") -> dict:
        """Simulate a user request for latency and bandwidth testing."""
        pass

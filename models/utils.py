import random
from models.user import User
from  skyfield.api import  wgs84

# change constants names here if need
UPDATE_LENGTH_IN_SEC = 60
FILE_NAME = '3le-3000'
COORDINATE_FILE = 'locations_coordinates.json'


def generate_ground_users(num_users):
    """
    Generate a list of users on the Earth's surface with calculated XYZ coordinates.

    :param num_users: Number of users to generate.
    :return: List of user dictionaries containing name, latitude, longitude, and XYZ coordinates.
    """
    users = []

    for i in range(num_users):
        user_name = f"user_{i}"  # Assign a unique name to each user
        lat = random.uniform(-90, 90)  # Random latitude
        lon = random.uniform(-180, 180)  # Random longitude

        # Calculate XYZ coordinates assuming elevation at ground level (Earth's surface)
        position = wgs84.latlon(lat, lon)
        xyz = position.itrs_xyz.km  # Convert to Cartesian coordinates in kilometers

        users.append(User(user_name,  lat=lat , lon =lon , xyz=xyz))

    return users


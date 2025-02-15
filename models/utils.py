import random
from models.user import User
from  skyfield.api import  wgs84
import  numpy as np
import random


# change constants names here if need
UPDATE_LENGTH_IN_SEC = 20       # in seconds
FILE_NAME = '3le-1000'          # 3le-10, 3le-100 , 3le-1000 , 3le-3000 3le
COORDINATE_FILE = 'locations_coordinates.json'

def generate_ground_users_1(num_users):
    """
    # distributed Users
    Generate a list of users on the Earth's surface

    :param num_users: Number of users to generate.
    :return: List of user  containing name, latitude, longitude
    """
    users = []

    for i in range(num_users):
        user_name = f"u_{i}"  # Assign a unique name to each user
        lat = random.uniform(-70, 70)  # Random latitude
        lon = random.uniform(-180, 180)  # Random longitude

        user = User(user_name, lat , lon)
        users.append(user)
    # print("created " , num_users , " users") todo change to looger
    return users

def generate_ground_users_2(num_users):
    """
    Generate a list of users distributed within the continental United States

    :param num_users: Number of users to generate.
    :return: List of user containing name, latitude, longitude
    """
    users = []

    # Approximate latitude and longitude bounds of the continental United States
    lat_min, lat_max = 24.396308, 49.384358  # Southernmost and northernmost latitudes
    lon_min, lon_max = -125.0, -66.93457    # Westernmost and easternmost longitudes

    for i in range(num_users):
        user_name = f"u_{i}"  # Assign a unique name to each user
        lat = random.uniform(lat_min, lat_max)  # Random latitude within US bounds
        lon = random.uniform(lon_min, lon_max)  # Random longitude within US bounds

        user = User(user_name, lat, lon)
        users.append(user)
    print(f"Created {num_users} users distributed within the United States.")
    return users


def generate_ground_users_3(num_users):
    """
    Generate users distributed across multiple regions including Europe, USA, Canada,
    Australia, South America, and Southern Africa.

    :param num_users: Total number of users to generate.
    :return: List of users containing name, latitude, and longitude.
    """
    number_dist = num_users // 5  # Divide users equally across regions



    # Define bounding boxes for regions
    regions = {
        "Europe": {"lat_min": 35.0, "lat_max": 60.0, "lon_min": -10.0, "lon_max": 30.0},  # Excluding Russia
        "USA": {"lat_min": 25.0, "lat_max": 49.0, "lon_min": -125.0, "lon_max": -66.0},
        "Canada": {"lat_min": 50.0, "lat_max": 70.0, "lon_min": -140.0, "lon_max": -50.0},
        "Australia": {"lat_min": -35.0, "lat_max": -15.0, "lon_min": 113.0, "lon_max": 153.0},
        "Southern Africa": {"lat_min": -30.0, "lat_max": -15.0, "lon_min": 15.0, "lon_max": 40.0},  # Around Zimbabwe
    }

    users = []

    # Generate users for each region
    for region, bounds in regions.items():
        for i in range(number_dist):
            lat = random.uniform(bounds["lat_min"], bounds["lat_max"])
            lon = random.uniform(bounds["lon_min"], bounds["lon_max"])
            user = User(f"{region.lower()}_{i}", lat, lon)
            users.append(user)

    print(f"Created users: {len(users)}")
    return users


# def generate_ground_users_3(num_users):
#     """
#     Generate users distributed across Europe, USA, Canada, and Australia.
#
#     :param num_users: Total number of users to generate.
#     :return: List of user containing name, latitude, and longitude.
#     """
#     number_dist = num_users // 4  # Divide users equally across regions
#
#     # Define bounding boxes for regions
#     regions = {
#         "Europe": {"lat_min": 35.0, "lat_max": 70.0, "lon_min": -10.0, "lon_max": 40.0},
#         "USA": {"lat_min": 25.0, "lat_max": 49.0, "lon_min": -125.0, "lon_max": -66.0},
#         "Canada": {"lat_min": 50.0, "lat_max": 70.0, "lon_min": -140.0, "lon_max": -50.0},
#         "Australia": {"lat_min": -43.0, "lat_max": -10.0, "lon_min": 113.0, "lon_max": 153.0},
#     }
#
#     users = []
#
#     # Generate users for Europe
#     for i in range(number_dist):
#         lat = random.uniform(regions["Europe"]["lat_min"], regions["Europe"]["lat_max"])
#         lon = random.uniform(regions["Europe"]["lon_min"], regions["Europe"]["lon_max"])
#         user = User(f"eu_{i}", lat, lon)
#         users.append(user)
#
#
#     # Generate users for USA
#     for i in range(number_dist):
#         lat = random.uniform(regions["USA"]["lat_min"], regions["USA"]["lat_max"])
#         lon = random.uniform(regions["USA"]["lon_min"], regions["USA"]["lon_max"])
#         user = User(f"usa_{i}", lat, lon)
#         users.append(user)
#
#     # Generate users for Canada
#     for i in range(number_dist):
#         lat = random.uniform(regions["Canada"]["lat_min"], regions["Canada"]["lat_max"])
#         lon = random.uniform(regions["Canada"]["lon_min"], regions["Canada"]["lon_max"])
#         user = User(f"can_{i}", lat, lon)
#         users.append(user)
#
#     # Generate users for Australia
#     for i in range(number_dist):
#         lat = random.uniform(regions["Australia"]["lat_min"], regions["Australia"]["lat_max"])
#         lon = random.uniform(regions["Australia"]["lon_min"], regions["Australia"]["lon_max"])
#
#         user = User(f"aus_{i}", lat, lon)
#         users.append(user)
#
#     print(f"Created users: {len(users)}")
#     return users

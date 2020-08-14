import random
import json
import os
import math


# Global Variable N, M for Grid Size

N, M = (0, 0)

# UAV communication threshold

UAV_to_UAV_comm = 0

# Ground user Communication threshold

rad = 0

# Number of users

number_users = 0


def update_files(N, M, number_users, UAV_to_UAV_comm, rad):
    """
    Function: update_files\n
    Parameters: (N, M) -> Size of the grid, number_users -> number of users in the grid, UAV_to_UAV_com -> UAV To UAV communication threshold, rad -> Radius of UAVs\n
    Functionality: Writes the correspoinding data to scenario_input.json file
    """
    scenario_data = {}
    parent_dir = os.getcwd()
    dir_name = 'input_files'
    file_name = 'scenario_input.json'
    with open(os.path.join(parent_dir, dir_name, file_name), 'r') as file_pointer:
        scenario_data = json.load(file_pointer)
    scenario_data['N'] = N
    scenario_data['M'] = M
    file_path = os.path.join(parent_dir, dir_name, file_name)
    with open(file_path, 'w') as file_pointer:
        json.dump(scenario_data, file_pointer)



def take_input():
    """
    Function: take_input\n
    Parameters: None\n
    Functionality: reads user_location.json (for Grid size and number of users) and scenario_input.json for Radius values\n
    """
    global N, M, rad, UAV_to_UAV_comm, number_users
    user_input={}
    parent_dir=os.getcwd()
    dir_name='input_files'
    file_name='user_location.json'
    with open(os.path.join(parent_dir, dir_name, file_name), 'r') as file_pointer:
        user_input=json.load(file_pointer)
    N=user_input['N']
    M=user_input['M']
    number_users=user_input['Number of User']
    scenario_data={}
    file_name='scenario_input.json'
    with open(os.path.join(parent_dir, dir_name, file_name), 'r') as file_pointer:
        scenario_data=json.load(file_pointer)
    UAV_to_UAV_comm=scenario_data['UAV_to_UAV_threshold']
    rad=scenario_data['radius_UAV']
    update_files(N, M, number_users, UAV_to_UAV_comm, rad)


take_input()

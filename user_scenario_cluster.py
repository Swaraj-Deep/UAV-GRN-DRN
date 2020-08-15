import random
import json
import os
import math


# Global Variable N, M for Grid Size

N, M = (0, 0)

# Number of users

number_users = 0

# Ground user UAV communication threshold

radius_UAV = 0

# User locations

user_loc_lst = []

def generate_clusters():
    """
    Function: generate_clusters\n
    Parameters: None\n
    Functionality: Generate clusters for users location\n
    """
    




def update_files():
    """
    Function: update_files\n
    Parameters: None\n
    Functionality: Writes the correspoinding data to scenario_input.json file
    """
    global N, M
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
    generate_clusters()

def take_input():
    """
    Function: take_input\n
    Parameters: None\n
    Functionality: reads user_location.json (for Grid size and number of users) and scenario_input.json for Radius values\n
    """
    global N, M, number_users, radius_UAV
    user_input = {}
    parent_dir = os.getcwd()
    dir_name = 'input_files'
    file_name = 'user_location.json'
    with open(os.path.join(parent_dir, dir_name, file_name), 'r') as file_pointer:
        user_input = json.load(file_pointer)
    N = user_input['N']
    M = user_input['M']
    number_users = user_input['Number of User']
    scenario_data = {}
    file_name = 'scenario_input.json'
    with open(os.path.join(parent_dir, dir_name, file_name), 'r') as file_pointer:
        scenario_data = json.load(file_pointer)
    UAV_to_UAV_comm = scenario_data['radius_UAV']
    update_files(N, M, number_users)


take_input()

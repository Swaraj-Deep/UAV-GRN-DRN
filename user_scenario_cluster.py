import random
import json
import os
import math
import move_endpoint.movement


# Global Variable N, M for Grid Size

N, M = (0, 0)

# Number of users

number_users = 0

# Ground user UAV communication threshold

radius_UAV = 0

# User locations

user_loc_lst = []

# Cell Size 

cell_size = 0

# Unit Multiplier

unit_mul = 0


def write_to_file():
    """
    Function: write_to_file\n
    Parameters: None\n
    Functionality: writes the user_location to file\n
    """
    global number_users, user_loc_lst
    write_data = {}
    write_data["Number of Ground users"] = number_users
    write_data["Position of Ground users"] = user_loc_lst
    parent_dir = os.getcwd()
    dir_name = "input_files"
    file_name = "user_input.json"
    with open(os.path.join(parent_dir, dir_name, file_name), 'w') as file_pointer:
        json.dump(write_data, file_pointer)


def generate_user_points():
    """
    Function: generate_user_points\n
    Parameters: None\n
    Returns: list of user location\n
    """
    global number_users, user_loc_lst, N, M, radius_UAV, unit_mul, cell_size
    c_a = round(random.uniform(0, N - 1), 2)
    c_b = round(random.uniform(0, M - 1), 2)
    pos1 = (c_a, c_b)
    user_loc_lst.append(f'{c_a} {c_b}')
    number_user_in_cluster = random.randint(10, 31)
    users_left = number_users - len(user_loc_lst)
    if number_user_in_cluster > users_left:
        number_user_in_cluster = users_left
    lst_rad_mul = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
    pos = random.randint(1, len(lst_rad_mul)) - 1
    cluster_radius = radius_UAV * lst_rad_mul[pos]
    temp_user_lst = []
    while len(temp_user_lst) < number_user_in_cluster:
        a = round(random.uniform(0, N - 1), 2)
        b = round(random.uniform(0, M - 1), 2)
        pos2 = (a, b)
        if move_endpoint.movement.get_euc_dist(pos1, pos2) * cell_size <= cluster_radius:
            temp_user_lst.append(f'{a} {b}')
    return temp_user_lst


def generate_clusters():
    """
    Function: generate_clusters\n
    Parameters: None\n
    Functionality: Generate user location\n
    """
    global N, M, number_users, user_loc_lst, radius_UAV
    while len(user_loc_lst) < number_users:
        user_loc_lst += generate_user_points()
    write_to_file()


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
    global N, M, number_users, radius_UAV, cell_size, unit_mul
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
    cell_size = scenario_data['cell_size']
    unit_mul = scenario_data['unit_multiplier']
    radius_UAV = scenario_data['radius_UAV'] * unit_mul
    cell_size *= unit_mul
    update_files()


if __name__ == "__main__":
    take_input()

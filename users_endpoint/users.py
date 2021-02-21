import json
import move_endpoint.movement
import pandas as pd

# Global Variables declarations

# Variable to hold the number of ground users

number_ground_users = 0

# Varialbe to hold the maximum density in the grid

max_density = -1

# Variable to hold the position of the maximum density in the grid

max_pos = (-1, -1)

# Dictionary containing Ground User Positions
# Key in this dictionary is Position of the ground user
# Value in this dictionary is Ground User at that position

ground_user_pos = {}

# Dictionary containing Number of users connected from a given cell
# Key in this dictionary is cell location
# Value is the number of users which are connected from that location

ground_cell_connections = {}

# Dictionary containing list users connected from a given cell
# Key in this dictionary is cell location
# Value is the list of users which are connected from that location

users_cell_connections = {}

# Dictionary containing Grid Position and number of ground users
# Key in this dictionary is the cell in grid and value in this grid is the list of ground users
grid_ground_users = {}


def init():
    """
    Function: init\n
    Parameter: None\n
    Returns: None\n
    Functionality: makes number of ground Users and their locations globally available\n
    """
    global grid_ground_users
    global number_ground_users
    global ground_user_pos
    scenario_data = {}
    N = 0
    M = 0
    radius_UAV = 0
    cell_size = 0
    unit_mul = 0
    with open('input_files/scenario_input.json', 'r') as file_pointer:
        scenario_data = json.load(file_pointer)
    N = scenario_data['N']
    M = scenario_data['M']
    radius_UAV = scenario_data['radius_UAV']
    cell_size = scenario_data['cell_size']
    unit_mul = scenario_data['unit_multiplier']
    radius_UAV *= unit_mul
    cell_size *= unit_mul
    with open('input_files/user_input.json', 'r') as file_pointer:
        file_data = json.load(file_pointer)
        number_ground_users = int(file_data['Number of Ground users'])
        pos_data = file_data['Position of Ground users']
        for index, pos in enumerate(pos_data):
            x, y = map(float, pos.split(' '))
            ground_user_pos[(x, y)] = index + 1
            int_part_x = int(x * 100 // 100)
            int_part_y = int(y * 100 // 100)
            if (int_part_x, int_part_y) not in grid_ground_users:
                grid_ground_users[(int_part_x, int_part_y)] = []
                grid_ground_users[(int_part_x, int_part_y)].append((x, y))
            else:
                grid_ground_users[(int_part_x, int_part_y)].append((x, y))
    set_cell_connections(radius_UAV, N, M, cell_size)


def get_number_ground_users():
    """
    Function: get_number_ground_users\n
    Parameter: None\n
    Returns: number of ground users\n
    """
    global number_ground_users
    return number_ground_users


def get_standard_deviation():
    """
    Function: get_standard_deviation\n
    Parameters: None\n
    Returns: Standard Deviation of the distance between user locations\n
    """
    global ground_user_pos
    locations = [loc for loc, user in ground_user_pos.items()]
    distances = [move_endpoint.movement.get_euc_dist(
        loc1, loc2) for loc1 in locations for loc2 in locations if loc1 != loc2]
    distances_df = pd.DataFrame(distances)
    return distances_df.describe()[0]['std']


def set_cell_helper(i, j, radius_UAV, N, M, cell_size):
    """
    Function: set_cell_helper\n
    Parameters\n
    i -> ith row of the grid\n
    j -> jth row of the grid\n
    radius_UAV -> radius of the UAV\n
    N -> number of rows in the grid\n
    M -> number of columns in the grid\n
    cell_size -> size of each cell in the grid\n
    Returns: a tuple of count of connected users and list of users which are connected from that cell\n
    """
    global grid_ground_users
    radius_UAV //= cell_size
    up = int(max(0, i - radius_UAV))
    left = int(max(0, j - radius_UAV))
    down = int(min(N - 1, i + radius_UAV))
    right = int(min(M - 1, j + radius_UAV))
    count = 0
    user_list = []
    for i in range(up, down + 1):
        for j in range(left, right + 1):
            if (i, j) in grid_ground_users:
                count += len(grid_ground_users[(i, j)])
                user_list += grid_ground_users[(i, j)]
    return (count, user_list)


def set_cell_connections(radius_UAV, N, M, cell_size):
    """
    Function: set_cell_connections\n
    Parameters: radius_UAV -> radius of the UAV, N -> number of rows in the grid, M -> number of columns in the grid, cell_size -> cell size of one grid\n
    Functionality: makes ground_cell_connections and user_cell_connections globally available
    """
    global max_density
    global max_pos
    global ground_cell_connections, users_cell_connections
    for i in range(N):
        for j in range(M):
            expected_desity, user_list = set_cell_helper(
                i, j, radius_UAV, N, M, cell_size)
            if expected_desity > max_density:
                max_density = expected_desity
                max_pos = (i, j)
            ground_cell_connections[(i, j)] = expected_desity
            users_cell_connections[(i, j)] = user_list


def get_users_cell_connections(loc):
    """
    Function: get_user_cell_connections\n
    Parameter: loc -> location in the grid\n
    Returns: the list of ground users which can be reached from passed location in the location is there else returns empty list\n
    """
    global users_cell_connections
    if loc in users_cell_connections:
        return users_cell_connections[loc]
    return []


def get_max_pos_density():
    """
    Function: get_max_pos_density\n
    Returns: a tuple of maximum user density and position\n
    """
    global max_density
    global max_pos
    return (max_pos, max_density)


if __name__ == "__main__":
    init()

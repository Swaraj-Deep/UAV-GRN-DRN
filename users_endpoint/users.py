import json

# Global Variables declarations

# Variable to hold the number of ground users

number_ground_users = 0

# Varialbe to hold the maximum density in the grid

max_density = -1

# Variable to hold the position of the maximum density in the grid

max_pos = (-1, -1)

# Dictionary containing Ground User Positions
# Key in this dictionary is Ground User
# Value in this dictionary is Position of the ground user

ground_user_pos = {}

# Dictionary containing Number of users connected from a given cell
# Key in this dictionary is cell location
# Value is the number of users which are connected from that location

ground_cell_connections = {}

# Dictionary containing list users connected from a given cell
# Key in this dictionary is cell location
# Value is the list of users which are connected from that location

users_cell_connections = {}


def init(radius_UAV, N, M):
    """
    Function: init\n
    Parameter: radius_UAV -> radius of the UAV, N -> Number of rows in the grid, M -> number of columns in the grid\n
    Returns: None\n
    Functionality: makes number of ground Users and their locations globally available\n
    """
    global number_ground_users
    global ground_user_pos
    with open('input_files/user_input.json', 'r') as file_pointer:
        file_data = json.load(file_pointer)
        number_ground_users = file_data['Number of Ground users']
        pos_data = file_data['Position of Ground users']
        for index, pos in enumerate(pos_data):
            x, y = map(int, pos.split(' '))
            ground_user_pos[(x, y)] = index + 1
    set_cell_connections(radius_UAV, N, M)


def get_number_ground_users():
    """
    Function: get_number_ground_users\n
    Parameter: None\n
    Returns: number of ground users\n
    """
    global number_ground_users
    return number_ground_users


def get_ground_users_pos(loc):
    """
    Function: get_ground_users_pos\n
    Parameter: loc -> location in the grid\n
    Returns: position of ground users if position is in the grid else returns zero\n
    """
    global ground_user_pos
    if loc in ground_user_pos:
        return ground_user_pos[loc]
    return 0


def set_cell_helper(i, j, radius_UAV, N, M):
    """
    Function: set_cell_helper\n
    Parameters\n
    i -> ith row of the grid\n
    j -> jth row of the grid\n
    radius_UAV -> radius of the UAV\n
    N -> number of rows in the grid\n
    M -> number of columns in the grid\n
    Returns: a tuple of count of connected users and list of users which are connected from that cell
    """
    up = max(0, i - radius_UAV)
    left = max(0, j - radius_UAV)
    down = min(N - 1, i + radius_UAV)
    right = min(M - 1, j + radius_UAV)
    count = 0
    user_list = []
    for i in range(up, down + 1):
        for j in range(left, right + 1):
            if (i, j) in ground_user_pos:
                count += 1
                user_list.append(ground_user_pos[(i, j)])
    return (count, user_list)


def set_cell_connections(radius_UAV, N, M):
    """
    Function: set_cell_connections\n
    Parameters: radius_UAV -> radius of the UAV, N -> number of rows in the grid, M -> number of columns in the grid\n
    Functionality: makes ground_cell_connections and user_cell_connections globally available
    """
    global max_density
    global max_pos
    for i in range(N):
        for j in range(M):
            expected_desity, user_list = set_cell_helper(
                i, j, radius_UAV, N, M)
            if expected_desity > max_density:
                max_density = expected_desity
                max_pos = (i, j)
            ground_cell_connections[(i, j)] = expected_desity
            users_cell_connections[(i, j)] = user_list


def get_ground_cell_connections(loc):
    """
    Function: get_ground_cell_connections\n
    Parameter: loc -> location in the grid\n
    Returns: the number of ground users which can be reached from passed location in the location is there else returns zero\n
    """
    global ground_cell_connections
    if loc in ground_cell_connections:
        return ground_cell_connections[loc]
    return 0


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

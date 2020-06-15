import json
import random
import numpy as np
import os
import os.path
import networkx as nx
import users_endpoint.users
import grn_endpoint.grn_info
import move_endpoint.movement
import matplotlib.pyplot as plt

# Global variables declaration

# Threshold for UAVs i.e each UAV must be placed at least this distance away

t = 0

# Number of rows and columns in the grid

N = 0
M = 0

# Exploration and exploitation rate of the agent

epsilon = 0

# Learning rate of the agent

learning_rate = 0

# Discount factor for the agent

discount_factor = 0

# Number of UAVs

number_UAV = 0

# Variable to hold the UAV to UAV Threshold

UAV_to_UAV_threshold = 0

# Radius of the UAV

radius_UAV = 0

# Power of the UAV

power_UAV = 0

# Maximum iteration for the algorithm

max_iter = 0

# Dictionary to hold the location of jth UAV
# Key in this dictionary is the UAV_node
# Value is the location in which it is placed

UAV_location = {}

# List to contain already connected ground users

ground_placed = []


def init():
    """
    Function: init
    Functionality: Sets all the global variables
    """
    global N
    global M
    global t
    global epsilon
    global learning_rate
    global discount_factor
    global max_iter
    global number_UAV
    global radius_UAV
    global UAV_to_UAV_threshold
    global power_UAV
    with open('input_files/scenario_input.json', 'r') as file_pointer:
        file_data = json.load(file_pointer)
        N = file_data['N']
        M = file_data['M']
        t = file_data['t']
        epsilon = file_data['epsilon']
        learning_rate = file_data['learning_rate']
        discount_factor = file_data['discount_factor']
        max_iter = file_data['max_iter']
        number_UAV = file_data['number_UAV']
        radius_UAV = file_data['radius_UAV']
        UAV_to_UAV_threshold = file_data['UAV_to_UAV_threshold']
        power_UAV = file_data['power_UAV']
    users_endpoint.users.init(radius_UAV, N, M)


def is_equal(list_1, list_2):
    """
    Function: is_equal\n
    Parameters: list_1 -> first list, list_2 -> second list\n
    Return: True if both list_1 and list_2 are equal else False
    """
    if len(list_1) != len(list_2):
        return False
    len_list = 0
    for item in list_2:
        if item in list_1:
            len_list += 1
    if len_list == len(list_1):
        return True
    return False


def reward_function(UAV_node, placed, pos_i):
    """
    Function: reward_function\n
    Parameters: UAV_node -> the UAV which needs to be placed, placed -> list of already placed UAVs, pos_i -> current position of the UAV_node\n
    Returns: the reward for this configuration\n
    """
    global t
    global UAV_to_UAV_threshold
    global power_UAV
    neg_reward = 1
    pos_reward = 1
    ground_users = users_endpoint.users.get_number_ground_users()
    user_served_temp = set()
    connectivity = users_endpoint.users.get_ground_cell_connections(pos_i)
    if connectivity == 0:
        neg_reward += 9999999
    user_connected_i = users_endpoint.users.get_users_cell_connections(pos_i)
    for j in placed:
        pos_j = UAV_location[j]
        user_connected_j = users_endpoint.users.get_users_cell_connections(
            pos_j)
        for user in user_connected_j:
            user_served_temp.add(user)
        if is_equal(user_connected_i, user_connected_j):
            neg_reward += 999999
        else:
            pos_reward += 99999
    if len(user_served_temp) / ground_users < 1:
        neg_reward += 999999
    for j in placed:
        pos_j = UAV_location[j]
        dist_uav = move_endpoint.movement.get_dist_UAV(pos_i, pos_j)
        if dist_uav == 0 or dist_uav <= t:
            neg_reward += 99999999 * -999
        # if dist_uav > t and dist_uav <= UAV_to_UAV_threshold:
        #     if grn_endpoint.grn_info.is_edge_grn(UAV_node, j) or grn_endpoint.grn_info.is_edge_grn(j, UAV_node):
        #         pos_reward += 99999
        #     else:
        #         pos_reward += 9999
    reward = pos_reward / neg_reward
    reward *= power_UAV
    return reward


def q_learn(UAV_node, placed):
    """
    Function: q_learn\n
    Parameters: UAV_node -> UAV_node which is to be placed, placed -> list of already placed UAV_nodes\n
    Return: the optimal position where the UAV_node needs to be placed\n
    """
    global N
    global M
    global epsilon
    global learning_rate
    global discount_factor
    global max_iter
    Q = np.zeros((N * M, 4))
    loc = move_endpoint.movement.get_random_location(N, M)
    for iterations in range(max_iter):
        x, y, action = move_endpoint.movement.get_random_move(loc, N, M)
        loc = (x, y)
        if random.uniform(0, 1) <= epsilon:
            index = move_endpoint.movement.map_2d_to_1d(loc, N)
            Q[index, action] = reward_function(UAV_node, placed, loc)
        else:
            index = move_endpoint.movement.map_2d_to_1d(loc, N)
            reward = reward_function(UAV_node, placed, loc)
            Q[index, action] = Q[index, action] + learning_rate * \
                (reward + discount_factor *
                 np.max(Q[index, :]) - Q[index, action])
    max_reward = -1
    max_pos = -1
    for index, rows in enumerate(Q):
        expected_max = np.max(rows)
        if expected_max > max_reward:
            max_reward = expected_max
            max_pos = index
    x, y = move_endpoint.movement.map_1d_to_2d(max_pos, N, M)
    # print(f"Node: {UAV_node}\nMaximum reward value: {max_reward}")
    return (x, y)


def simulation():
    """
    Function: simulation\n
    Parameters: None\n
    Functionality: Simulates the network
    """
    placed = [1]
    unplaced = []
    max_pos, max_density = users_endpoint.users.get_max_pos_density()
    UAV_location[1] = max_pos
    user_list = users_endpoint.users.get_users_cell_connections(max_pos)
    for user in user_list:
        if user not in ground_placed:
            ground_placed.append(user)
    for UAV_node in range(2, number_UAV + 1):
        unplaced.append(UAV_node)
    for UAV_node in unplaced:
        loc = q_learn(UAV_node, placed)
        UAV_location[UAV_node] = loc
        placed.append(UAV_node)
        user_list = users_endpoint.users.get_users_cell_connections(loc)
        for user in user_list:
            if user not in ground_placed:
                ground_placed.append(user)
    write_output(placed)


def write_output(placed):
    """
    Function: write_output
    Parameters: placed -> list of already placed UAVs
    Functionality: write the output to the respective files
    """
    file_num = len([name for name in os.listdir(
        './output_files')])
    text_file_name = './output_files/' + \
        'Output_text' + str(file_num // 2) + '.txt'
    graph_file_name = './output_files/' + \
        'Output_graph' + str(file_num // 2) + '.png'
    text_file_data = []
    for UAV_node, loc in UAV_location.items():
        text_file_data.append(
            f'UAV: {UAV_node} can serve users: {users_endpoint.users.get_users_cell_connections(loc)} when placed at {loc}\n')
    text_file_data.append(
        f'Total Number of users served: {len(ground_placed)}\nList of users: {sorted(ground_placed)}')
    with open(text_file_name, 'w') as file_pointer:
        file_pointer.writelines(text_file_data)
    G = nx.Graph()
    for node in placed:
        G.add_node(node)
    for node1 in placed:
        for node2 in placed:
            if move_endpoint.movement.get_dist_UAV(UAV_location[node1], UAV_location[node2]) <= UAV_to_UAV_threshold:
                G.add_edge(node1, node2)
    nx.draw(G, with_labels=True)
    plt.savefig(graph_file_name)


if __name__ == "__main__":
    init()
    simulation()

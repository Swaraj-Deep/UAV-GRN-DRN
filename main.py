import json
import random
import numpy as np
import os
import os.path
import networkx as nx
import users_endpoint.users
import grn_endpoint.grn_info
import move_endpoint.movement
import reward_endpoint.rewards
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

# Decay factor for exploration rate

decay_factor = 0

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
    global decay_factor
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
        decay_factor = file_data['decay_factor']
        max_iter = file_data['max_iter']
        number_UAV = file_data['number_UAV']
        radius_UAV = file_data['radius_UAV']
        UAV_to_UAV_threshold = file_data['UAV_to_UAV_threshold']
        power_UAV = file_data['power_UAV']
    users_endpoint.users.init(radius_UAV, N, M)


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
    global decay_factor
    global max_iter
    Q = np.zeros((N * M, 4))
    loc = move_endpoint.movement.get_random_location(N, M)
    for iterations in range(max_iter):
        x, y, action = move_endpoint.movement.get_random_move(loc, N, M)
        loc = (x, y)
        if random.uniform(0, 1) <= epsilon:
            index = move_endpoint.movement.map_2d_to_1d(loc, N)
            Q[index, action] = reward_endpoint.rewards.reward_function(
                UAV_node, placed, loc, UAV_location, t, power_UAV, UAV_to_UAV_threshold)
        else:
            index = move_endpoint.movement.map_2d_to_1d(loc, N)
            reward = reward_endpoint.rewards.reward_function(
                UAV_node, placed, loc, UAV_location, t, power_UAV, UAV_to_UAV_threshold)
            Q[index, action] = Q[index, action] + learning_rate * \
                (reward + decay_factor *
                 np.max(Q[index, :]) - Q[index, action])
    max_reward = -1
    max_pos = -1
    for index, rows in enumerate(Q):
        expected_max = np.max(rows)
        if expected_max > max_reward:
            max_reward = expected_max
            max_pos = index
    x, y = move_endpoint.movement.map_1d_to_2d(max_pos, N, M)
    print(f"Node: {UAV_node}\nMaximum reward value: {max_reward}")
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

import json
import random
import numpy as np
import users_endpoint.users
import grn_endpoint.grn_info
import move_endpoint.movement

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

# Maximum iteration for the algorithm

max_iter = 0

# Dictionary to hold the location of jth UAV
# Key in this dictionary is the UAV_node
# Value is the location in which it is placed

UAV_location = {}

# List to contain already connected ground users

ground_placed = []


def reward_function(UAV_node, placed, pos_i):
    """
    Function: reward_function\n
    Parameters: UAV_node -> the UAV which needs to be placed, placed -> list of already placed UAVs, pos_i -> current position of the UAV_node\n
    Returns: the reward for this configuration\n
    """
    global t
    global UAV_to_UAV_threshold
    neg_reward = 0
    pos_reward = 0
    for j in placed:
        pos_j = UAV_location[j]
        if move_endpoint.movement.get_dist_UAV(pos_1=pos_i, pos_2=pos_j) < t:
            neg_reward += 99
        else:
            pos_reward += 999
    user_served = users_endpoint.users.get_users_cell_connections(pos_i)
    for users in user_served:
        if users not in ground_placed:
            pos_reward += 9999
        else:
            pos_reward += 9
    for j in placed:
        pos_j = UAV_location[j]
        if grn_endpoint.grn_info.GRN_edges(UAV_node, j) and move_endpoint.movement.get_dist_UAV(pos_i, pos_j) < UAV_to_UAV_threshold:
            pos_reward += 9999
        else:
            pos_reward += 99
    for node, pos in UAV_location.items():
        if pos == pos_i:
            neg_reward += 9999
    power_UAV = 5
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
        if random.uniform (0, 1) <= epsilon:
            index = move_endpoint.movement.map_2d_to_1d (loc, N)
            Q[index, action] = reward_function(UAV_node, placed, loc)
        else:
            index = move_endpoint.movement.map_2d_to_1d (loc, N)
            reward = reward_function (UAV_node, placed, loc)
            Q[index, action] = Q[index, action] + learning_rate * (reward + discount_factor * np.max (Q[index, :]) - Q[index, action])
    max_reward = -1
    max_pos = -1
    for state in Q:
        expected_max = np.max(Q[state, :])
        if expected_max > max_reward:
            max_reward = expected_max
            max_pos = state
    x, y = move_endpoint.movement.map_1d_to_2d (max_pos, N, M)
    print(f"Node: {UAV_node}\nMaximum reward value: {max_reward}")
    return (x, y)


def simulation ():
    """
    Function: simulation\n
    Parameters: None\n
    Functionality: Simulates the network
    """
    placed = [1]
    unplaced = []
    max_pos, max_density = users_endpoint.users.get_max_pos_density
    UAV_location[1] = max_pos
    for UAV_node in range (2, number_UAV + 1):
        unplaced.append (UAV_node)
    for UAV_node in unplaced:
        loc = q_learn (UAV_node, placed)
        UAV_location[UAV_node] = loc
        placed.append (UAV_node)
    for UAV_node, location in UAV_location.items():
        print (f'UAV: {UAV_node} can serve users: {users_endpoint.users.get_users_cell_connections(location)}')

def init():
    """
    Function: init
    Functionality: Sets all the global variables
    """
    with open ('../input_files/scenario_input.json', 'r') as file_pointer:
        file_data = json.load (file_pointer)
    

if __name__ == "__main__":
    init()
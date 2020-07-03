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
    parent_dir = os.getcwd()
    folder_name = 'input_files'
    file_name = 'scenario_input.json'
    file_path = os.path.join(parent_dir, folder_name, file_name)
    with open(file_path, 'r') as file_pointer:
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
    grn_endpoint.grn_info.init()


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
    global power_UAV
    global UAV_location
    global radius_UAV
    global t
    Q = np.zeros((N * M, 15))
    # Centroid Location
    # loc = move_endpoint.movement.get_centroid_location(
    #     N, M, UAV_location, UAV_to_UAV_threshold)
    # Center Location
    # loc = move_endpoint.movement.get_center_location(N, M)
    # Random Location
    loc = move_endpoint.movement.get_random_location(N, M)
    # Vicinity Location
    # loc = move_endpoint.movement.get_vicinity_location(
    # N, M, UAV_location, UAV_to_UAV_threshold)
    epsilon_val = epsilon
    # low, medium, high power
    action_power = [0, 5, 10]
    for iterations in range(max_iter):
        x, y, action, power_factor = move_endpoint.movement.get_random_move(
            loc, N, M)
        loc = (x, y)
        action += action_power[power_factor]
        power_UAV += power_factor
        if random.uniform(0, 1) <= epsilon_val:
            index = move_endpoint.movement.map_2d_to_1d(loc, N)
            Q[index, action] = reward_endpoint.rewards.reward_function(
                UAV_node, placed, loc, UAV_location, t, power_UAV, UAV_to_UAV_threshold, radius_UAV, N, M)
        else:
            index = move_endpoint.movement.map_2d_to_1d(loc, N)
            reward = reward_endpoint.rewards.reward_function(
                UAV_node, placed, loc, UAV_location, t, power_UAV, UAV_to_UAV_threshold, radius_UAV, N, M)
            Q[index, action] = Q[index, action] + learning_rate * \
                (reward + decay_factor *
                 np.max(Q[index, :]) - Q[index, action])
        epsilon_val *= decay_factor
    max_reward = -1
    max_pos = -1
    for index, rows in enumerate(Q):
        expected_max = np.max(rows)
        if expected_max >= max_reward:
            max_reward = expected_max
            max_pos = index
    x, y = move_endpoint.movement.map_1d_to_2d(max_pos, N, M)
    print(f"Node: {UAV_node}\nMaximum reward value: {max_reward}")
    return (x, y)


def done_simulation(ground_placed, placed):
    """
    Function: done_simulation\n
    Parameters: ground_placed -> list of users alredy placed, placed -> list of UAVs placed\n
    Returns: True if simulation is done\n
    """
    ground_users = users_endpoint.users.get_number_ground_users()
    done_user_connectivity = False
    done_UAV_coverage = False
    if len(ground_placed) // ground_users == 1:
        done_user_connectivity = True
    UAV_G = nx.Graph()
    for node in placed:
        UAV_G.add_node(node)
    for node1 in placed:
        for node2 in placed:
            if move_endpoint.movement.get_dist_UAV(UAV_location[node1], UAV_location[node2]) <= UAV_to_UAV_threshold and node1 != node2:
                UAV_G.add_edge(node1, node2)
    if nx.number_connected_components(UAV_G) == 1:
        done_UAV_coverage = True
    return done_user_connectivity and done_UAV_coverage


def valid_loc(loc):
    """
    Function: valid_loc\n
    Parameter: loc -> location of the UAV being placed\n
    Return: true if that location is not occupied\n
    """
    global UAV_location
    for node, location in UAV_location.items():
        if location == loc:
            return False
    return True


def bruteforce(UAV_node, placed):
    """
    Function: bruteforce\n
    Parameters: UAV_node -> UAV_node which is to be placed, placed -> list of already placed UAV_nodes\n
    Functionality: bruteforce all the grid location\n
    """
    global N
    global M
    global radius_UAV
    global UAV_location
    global t
    global power_UAV
    max_reward = -999999
    max_pos = (-1, -1)
    for i in range(N):
        for j in range(M):
            loc = (i, j)
            reward = reward_endpoint.rewards.reward_function(
                UAV_node, placed, loc, UAV_location, t, power_UAV, UAV_to_UAV_threshold, radius_UAV, N, M)
            if reward > max_reward and valid_loc(loc):
                max_reward = reward
                max_pos = loc
    print(f"Node: {UAV_node}\nMaximum reward value: {max_reward}")
    return max_pos


def simulation():
    """
    Function: simulation\n
    Parameters: None\n
    Functionality: Simulates the network\n
    """
    # Till Now What we have done
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
        if done_simulation(ground_placed, placed):
            break
        loc = bruteforce(UAV_node, placed)
        UAV_location[UAV_node] = loc
        placed.append(UAV_node)
        user_list = users_endpoint.users.get_users_cell_connections(loc)
        for user in user_list:
            if user not in ground_placed:
                ground_placed.append(user)
    write_output(placed)

    # Placing One by One and Checking Graph
    # placed = [1]
    # max_pos, max_density = users_endpoint.users.get_max_pos_density()
    # UAV_location[1] = max_pos
    # user_list = users_endpoint.users.get_users_cell_connections(max_pos)
    # for user in user_list:
    #     if user not in ground_placed:
    #         ground_placed.append(user)
    # UAV_node = 1
    # while True:
    #     UAV_node += 1
    #     if done_simulation (ground_placed, placed):
    #         break
    #     loc = q_learn(UAV_node, placed)
    #     flag = True
    #     while flag:
    #         for UAV, location in UAV_location.items():
    #             if location == loc:
    #                 loc = q_learn(UAV_node, placed)
    #             else:
    #                 flag = False
    #             if done_simulation (ground_placed, placed):
    #                 flag = False
    #     UAV_location[UAV_node] = loc
    #     placed.append(UAV_node)
    #     user_list = users_endpoint.users.get_users_cell_connections(loc)
    #     for user in user_list:
    #         if user not in ground_placed:
    #             ground_placed.append(user)
    # write_output(placed)


def write_output(placed):
    """
    Function: write_output
    Parameters: placed -> list of already placed UAVs
    Functionality: write the output to the respective files
    """
    parent_dir = os.path.join(os.getcwd(), 'output_files')
    curr_dir = str(epsilon) + "_" + str(learning_rate) + \
        "_" + str(decay_factor)
    dir_path = os.path.join(parent_dir, curr_dir)
    try:
        os.mkdir(dir_path)
    except OSError as error:
        pass
    file_num = len([name for name in os.listdir(
        dir_path)])
    os.chdir(dir_path)
    text_file_name = 'Output_text' + str(file_num // 2) + '.txt'
    graph_file_name = 'Output_graph' + str(file_num // 2) + '.png'
    text_file_data = []
    text_file_data.append(
        f'Total Number of users served: {len(ground_placed)}\nList of users: {sorted(ground_placed)}\n')
    text_file_data.append (f'Total number of UAV used: {len(UAV_location)}\n')
    for UAV_node, loc in UAV_location.items():
        text_file_data.append(
            f'UAV: {UAV_node} can serve users: {users_endpoint.users.get_users_cell_connections(loc)} when placed at {loc}\n')
    UAV_G = nx.Graph()
    for node in placed:
        UAV_G.add_node(node)
    both_grn_UAV_edge_lst = []
    grn_edge_lst = []
    for node1 in placed:
        for node2 in placed:
            if move_endpoint.movement.get_dist_UAV(UAV_location[node1], UAV_location[node2]) <= UAV_to_UAV_threshold and node1 != node2:
                UAV_G.add_edge(node1, node2)
                gene_1 = grn_endpoint.grn_info.m(node1)
                gene_2 = grn_endpoint.grn_info.m(node2)
                if grn_endpoint.grn_info.is_edge_grn(gene_1, gene_2):
                    both_grn_UAV_edge_lst.append ((node1, node2))
            gene_1 = grn_endpoint.grn_info.m(node1)
            gene_2 = grn_endpoint.grn_info.m(node2)
            if grn_endpoint.grn_info.is_edge_grn(gene_1, gene_2) and (node1, node2) not in both_grn_UAV_edge_lst:
                grn_edge_lst.append ((node1, node2))
    total_edge = len (UAV_G.edges)
    if len(both_grn_UAV_edge_lst) > 0:
        text_file_data.append (f'Following are the edges which is present in both UAV and GRN netwrok:\n')
        for edge in both_grn_UAV_edge_lst:
            text_file_data.append (f'{edge}, ')
        text_file_data.append(f'\n')
    else:
        text_file_data.append (f'No edge is common in UAV and GRN network.\n')
    if len (grn_edge_lst) > 0:
        text_file_data.append (f'Following are the edges which is present in GRN but not in UAV network:\n')
        for edge in grn_edge_lst:
            text_file_data.append (f'{edge}, ')
        text_file_data.append(f'\n')
    else:
        text_file_data.append (f'There is no edge which is in GRN but not in the UAV network\n')
    text_file_data.append (f'Total Number of edges: {total_edge}\nPercentage of edge which is both in GRN and UAV: {(len(both_grn_UAV_edge_lst) / total_edge) * 100}\n')
    node_motif = grn_endpoint.grn_info.get_motif_dict (UAV_G)
    for node, motif in node_motif.items():
        text_file_data.append(f'Motif of UAV {node} is {motif}\n')
    e_motif = {}
    PI = 0
    for edge in UAV_G.edges:
        node1, node2 = edge
        e_motif[edge] = min(node_motif[node1], node_motif[node2])
        text_file_data.append(f'Edge {edge} has edge motif centrality of {e_motif[edge]}\n')
        PI = max(PI, e_motif[edge])
    text_file_data.append(f'Maximum Edge motif centrality is {PI}\n')
    with open(text_file_name, 'w') as file_pointer:
        file_pointer.writelines(text_file_data)
    nx.draw(UAV_G, with_labels=True)
    plt.savefig(graph_file_name)


if __name__ == "__main__":
    init()
    simulation()

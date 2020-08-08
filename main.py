import json
import random
import numpy as np
import os
import time
import os.path
import networkx as nx
import users_endpoint.users
import grn_endpoint.grn_info
import move_endpoint.movement
import reward_endpoint.rewards
import matplotlib.pyplot as plt

# Global variables declaration
# User coverage threshold

coverage_threshold = 0

# GRN Edge Similarity threshold

similarity_threshold = 0


# Start time of program

start_time = 0

# End time of program

end_time = 0

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
    global start_time
    global similarity_threshold
    global coverage_threshold
    start_time = time.time()
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
    dir_path = os.path.join(os.getcwd(), 'output_files')
    try:
        os.mkdir(dir_path)
    except OSError as error:
        pass
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
        coverage_threshold = file_data['coverage_threshold']
        similarity_threshold = file_data['similarity_threshold']
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
                UAV_node, placed, loc, UAV_location, t, power_UAV, UAV_to_UAV_threshold, radius_UAV, N, M, ground_placed)
        else:
            index = move_endpoint.movement.map_2d_to_1d(loc, N)
            reward = reward_endpoint.rewards.reward_function(
                UAV_node, placed, loc, UAV_location, t, power_UAV, UAV_to_UAV_threshold, radius_UAV, N, M, ground_placed)
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
    done_edge_similarity = False
    if len(ground_placed) / ground_users >= coverage_threshold:
        done_user_connectivity = True
    UAV_G = get_UAV_graph(placed)
    common_lst, _, grn_edge_lst, _ = similarity_criteria(
        UAV_G)
    total_edge_grn_SG = len(grn_edge_lst)
    if total_edge_grn_SG == 0:
        total_edge_grn_SG = 1
    if len(common_lst) / total_edge_grn_SG >= similarity_threshold:
        done_edge_similarity = True
    if nx.number_connected_components(UAV_G) == 1:
        done_UAV_coverage = True
    return done_user_connectivity and done_UAV_coverage and done_edge_similarity


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
    global ground_placed
    max_reward = -999999
    max_pos = (-1, -1)
    for i in range(N):
        for j in range(M):
            loc = (i, j)
            reward = reward_endpoint.rewards.reward_function(
                UAV_node, placed, loc, UAV_location, t, power_UAV, UAV_to_UAV_threshold, radius_UAV, N, M, ground_placed)
            if reward > max_reward and valid_loc(loc):
                max_reward = reward
                max_pos = loc
    return max_pos


def simulation():
    """
    Function: simulation\n
    Parameters: None\n
    Functionality: Simulates the network\n
    """
    global ground_placed
    placed = [1]
    unplaced = []
    max_pos, max_density = users_endpoint.users.get_max_pos_density()
    UAV_location[1] = max_pos
    print(f'Placed UAV {1}')
    user_list = users_endpoint.users.get_users_cell_connections(max_pos)
    for user in user_list:
        if user not in ground_placed:
            ground_placed.append(user)
    for UAV_node in range(2, number_UAV + 1):
        unplaced.append(UAV_node)
    for UAV_node in unplaced:
        loc = bruteforce(UAV_node, placed)
        UAV_location[UAV_node] = loc
        placed.append(UAV_node)
        print(f'Placed UAV {UAV_node}')
        if done_simulation(ground_placed, placed):
            break
        user_list = users_endpoint.users.get_users_cell_connections(loc)
        for user in user_list:
            if user not in ground_placed:
                ground_placed.append(user)
    write_output(placed)


def get_UAV_graph(placed):
    """
    Function: get_UAV_graph\n
    Parameters: placed -> list of already placed ground users\n:
    Returns: UAV graph at a particular point of time\n
    """
    UAV_G = nx.Graph()
    for node in placed:
        UAV_G.add_node(node)
    for node1 in placed:
        for node2 in placed:
            if move_endpoint.movement.get_dist_UAV(UAV_location[node1], UAV_location[node2]) <= UAV_to_UAV_threshold and node1 != node2:
                UAV_G.add_edge(node1, node2)
    return UAV_G


def similarity_criteria(UAV_G):
    """
    Function:similarity_criteria\n
    Parameter: UAV_G -> Current UAV graph\n
    Returns: A tuple of common edges, uncommon edges and edges which are in grn graph. Dictionary of reverse mapping is also returned\n
    """
    grn_node_lst = [grn_endpoint.grn_info.m(node) for node in UAV_G.nodes]
    reverse_mapping = {}
    for node in UAV_G.nodes:
        if grn_endpoint.grn_info.m(node) not in reverse_mapping:
            reverse_mapping[grn_endpoint.grn_info.m(node)] = node
    uncommon_lst = []
    common_lst = []
    grn_graph = grn_endpoint.grn_info.get_grn_graph()
    grn_SG = grn_graph.subgraph(grn_node_lst)
    grn_edge_lst = []
    for edge in grn_SG.edges:
        u, v = edge
        if (u, v) not in grn_edge_lst and (v, u) not in grn_edge_lst:
            grn_edge_lst.append((u, v))
    for edge in grn_edge_lst:
        u, v = edge
        if (reverse_mapping[u], reverse_mapping[v]) in UAV_G.edges or (reverse_mapping[v], reverse_mapping[u]) in UAV_G.edges:
            if (reverse_mapping[u], reverse_mapping[v]) not in common_lst and (reverse_mapping[v], reverse_mapping[u]) not in common_lst:
                common_lst.append((reverse_mapping[u], reverse_mapping[v]))
        else:
            if (reverse_mapping[u], reverse_mapping[v]) not in uncommon_lst and (reverse_mapping[v], reverse_mapping[u]) not in uncommon_lst:
                uncommon_lst.append((reverse_mapping[u], reverse_mapping[v]))
    return (common_lst, uncommon_lst, grn_edge_lst, reverse_mapping)


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
    graph_file_name = 'Output_graph' + str(file_num // 2) + '.json'
    image_path = os.path.join(dir_path, 'images')
    try:
        os.mkdir(image_path)
    except OSError as error:
        pass
    png_file_name = 'Output_graph' + str(file_num // 2) + '.png'
    text_file_data = []
    text_file_data.append(
        f'Total Number of users served: {len(ground_placed)}\nList of users: {sorted(ground_placed)}\n')
    text_file_data.append(f'Total number of UAV used: {len(UAV_location)}\n')
    for UAV_node, loc in UAV_location.items():
        text_file_data.append(
            f'UAV: {UAV_node} can serve users: {users_endpoint.users.get_users_cell_connections(loc)} when placed at {loc}\n')
    UAV_G = get_UAV_graph(placed)
    total_edge = len(UAV_G.edges)
    common_lst, uncommon_lst, grn_edge_lst, reverse_mapping = similarity_criteria(
        UAV_G)
    total_edge_grn_SG = len(grn_edge_lst)
    if total_edge_grn_SG == 0:
        total_edge_grn_SG = 1
    if total_edge == 0:
        total_edge = 1
    if len(common_lst) > 0:
        text_file_data.append(
            f'Following are the edges which is present in both UAV and GRN netwrok: ({len(common_lst)})\n')
        for edge in common_lst:
            text_file_data.append(f'{edge}, ')
        text_file_data.append(f'\n')
    else:
        text_file_data.append(f'No edge is common in UAV and GRN graph.\n')
    if len(uncommon_lst) > 0:
        text_file_data.append(
            f'Following are the edges which is present in GRN but not in UAV network: ({len(uncommon_lst)})\n')
        for edge in uncommon_lst:
            text_file_data.append(f'{edge}, ')
        text_file_data.append(f'\n')
    else:
        text_file_data.append(
            f'There is no edge which is in GRN but not in the UAV graph\n')
    text_file_data.append(
        f'Total Number of edges (in UAV Topology): {total_edge}\nPercentage of edge which is both in GRN and UAV: {(len(common_lst) / total_edge_grn_SG) * 100}\n')
    text_file_data.append(
        f'Following are the edges (in GRN Subgraph): {[(reverse_mapping[u], reverse_mapping[v]) for (u, v) in grn_edge_lst]}\n')
    text_file_data.append(
        f'Total Number of edges (in GRN Subgraph): {total_edge_grn_SG}\n')
    node_motif = grn_endpoint.grn_info.get_motif_dict(UAV_G)
    for node, motif in node_motif.items():
        text_file_data.append(f'Motif of UAV {node} is {motif}\n')
    e_motif = {}
    PI = 0
    for edge in UAV_G.edges:
        node1, node2 = edge
        e_motif[edge] = min(node_motif[node1], node_motif[node2])
        text_file_data.append(
            f'Edge {edge} has edge motif centrality of {e_motif[edge]}\n')
        PI = max(PI, e_motif[edge])
    text_file_data.append(f'Maximum Edge motif centrality is {PI}\n')
    nx.draw(UAV_G, with_labels=True)
    plt.savefig(os.path.join(image_path, png_file_name))
    graph_data = {}
    global radius_UAV
    graph_data["radius_UAV"] = radius_UAV
    user_served = {}
    for UAV, location in UAV_location.items():
        user_served[f"{UAV}"] = users_endpoint.users.get_users_cell_connections(
            location)
    ground_user_pos = users_endpoint.users.get_ground_user_pos_dict()
    ground_user = {}
    for loc, user in ground_user_pos.items():
        ground_user[user] = loc
    graph_data["user_loc"] = ground_user
    graph_data["edge_UAV"] = list(UAV_G.edges())
    graph_data["UAV_serves"] = user_served
    graph_data["gusers"] = sorted(ground_placed)
    global N
    global M
    global end_time
    graph_data['N'] = N
    graph_data['M'] = M
    graph_data['UAV_location'] = UAV_location
    with open(graph_file_name, 'w') as file_pointer:
        json.dump(graph_data, file_pointer)
    text_file_data.append(
        f'Standard Deviation of distances between users: {users_endpoint.users.get_standard_deviation()}\n')
    end_time = time.time()
    text_file_data.append(
        f'Total time to run the simulation: {end_time - start_time} seconds')
    with open(text_file_name, 'w') as file_pointer:
        file_pointer.writelines(text_file_data)


if __name__ == "__main__":
    print(f'Initialiazing the environment')
    init()
    simulation()

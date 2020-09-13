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
from matplotlib.backends.backend_pdf import PdfPages

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

# Cell Size of grid

cell_size = 0

# Unit multiplier

unit_mul = 0


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
    global cell_size, unit_mul
    parent_dir = os.getcwd()
    dir_path = os.path.join(parent_dir, 'output_files')
    try:
        os.mkdir(dir_path)
    except OSError as error:
        pass
    dir_path = os.path.join(parent_dir, 'graph_output_files')
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
        cell_size = file_data['cell_size']
        unit_mul = file_data['unit_multiplier']
    UAV_to_UAV_threshold *= unit_mul
    radius_UAV *= unit_mul
    cell_size *= unit_mul
    t *= unit_mul
    t //= cell_size
    users_endpoint.users.init()
    grn_endpoint.grn_info.init()


def done_simulation(ground_placed, placed):
    """
    Function: done_simulation\n
    Parameters: ground_placed -> list of users alredy placed, placed -> list of UAVs placed\n
    Returns: True if simulation is done\n
    """
    global coverage_threshold, similarity_threshold
    ground_users = users_endpoint.users.get_number_ground_users()
    done_user_connectivity = False
    done_UAV_coverage = False
    done_edge_similarity = False
    if len(set(ground_placed)) / ground_users >= coverage_threshold:
        done_user_connectivity = True
    UAV_G = get_UAV_graph(placed)
    common_lst, _, grn_edge_lst, _ = similarity_criteria(
        UAV_G)
    total_edge_grn_SG = len(grn_edge_lst)
    if total_edge_grn_SG == 0:
        total_edge_grn_SG = 1
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
    global ground_placed
    max_reward = -999999
    max_pos = (-1, -1)
    for i in range(N):
        for j in range(M):
            loc = (i, j)
            reward = reward_endpoint.rewards.reward_function_user(
                UAV_node, placed, loc, UAV_location, t, power_UAV, int(UAV_to_UAV_threshold // cell_size), int(radius_UAV // cell_size), N, M, set(ground_placed))
            if reward > max_reward and valid_loc(loc):
                max_reward = reward
                max_pos = loc
    return max_pos


def consider_user_coverage():
    """
    Function: consider_user_coverage\n
    Parameters: None\n
    Functionality: consider only user_coverage of the network\n
    """
    global ground_placed, number_UAV
    ground_users = users_endpoint.users.get_number_ground_users()
    placed = [1]
    unplaced = []
    max_pos, max_density = users_endpoint.users.get_max_pos_density()
    UAV_location[1] = max_pos
    print(f'Placed UAV {1}')
    user_list = users_endpoint.users.get_users_cell_connections(max_pos)
    for user in user_list:
        ground_placed.append(user)
    for UAV_node in range(2, number_UAV + 1):
        unplaced.append(UAV_node)
    for UAV_node in unplaced:
        if len(set(ground_placed)) / ground_users >= coverage_threshold:
            break
        if done_simulation(ground_placed, placed):
            break
        loc = bruteforce(UAV_node, placed)
        UAV_location[UAV_node] = loc
        placed.append(UAV_node)
        print(f'Placed UAV {UAV_node}')
        user_list = users_endpoint.users.get_users_cell_connections(loc)
        for user in user_list:
            ground_placed.append(user)
    return placed


def get_UAV_graph(placed):
    """
    Function: get_UAV_graph\n
    Parameters: placed -> list of already placed ground users\n:
    Returns: UAV graph at a particular point of time\n
    """
    global UAV_to_UAV_threshold, cell_size, UAV_location
    UAV_G = nx.Graph()
    for node in placed:
        UAV_G.add_node(node)
    for node1 in placed:
        for node2 in placed:
            if move_endpoint.movement.get_euc_dist(UAV_location[node1], UAV_location[node2]) <= int(UAV_to_UAV_threshold // cell_size) and node1 != node2:
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
    global radius_UAV, cell_size, UAV_to_UAV_threshold
    main_file_name = os.getcwd()
    parent_dir = os.path.join(main_file_name, 'output_files')
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
    if file_num == 0:
        file_num = 1
    text_file_name = 'Output_text' + str(file_num) + '.txt'
    image_path = os.path.join(dir_path, 'images')
    try:
        os.mkdir(image_path)
    except OSError as error:
        pass
    graph_file_name = 'Output_graph' + str(file_num) + '.pdf'
    text_file_data = []
    text_file_data.append(
        f'Total Number of users served: {len(set(ground_placed))}\nList of users: {sorted(set(ground_placed))}\n')
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
    UAV_topology = plt.figure(1)
    nx.draw(UAV_G, with_labels=True)
    global end_time
    text_file_data.append(
        f'Standard Deviation of distances between users: {users_endpoint.users.get_standard_deviation()}\n')
    end_time = time.time()
    text_file_data.append(
        f'Total time to run the simulation: {end_time - start_time} seconds')
    with open(text_file_name, 'w') as file_pointer:
        file_pointer.writelines(text_file_data)
    plt.close()
    g_x, g_y = get_user_location(main_file_name)
    UAV_guser_plot = plt.figure(2)
    plt.scatter(g_x, g_y, color='red')
    UAV_x = []
    UAV_y = []
    rad = int(radius_UAV // cell_size)
    for node, loc in UAV_location.items():
        a, b = loc
        UAV_x.append(a)
        UAV_y.append(b)
        c = plt.Circle((a, b), rad, color='green', fill=False)
        ax = plt.gca()
        ax.add_artist(c)
    plt.scatter(UAV_x, UAV_y, color='purple')
    for idx in range(len(UAV_x)):
        plt.annotate(f'{idx + 1}', (UAV_x[idx], UAV_y[idx]), color='black')
    for edge in UAV_G.edges:
        edge_x = []
        edge_y = []
        a, b = edge
        loc_a = UAV_location[a]
        loc_b = UAV_location[b]
        x1, y1 = loc_a
        x2, y2 = loc_b
        edge_x = [x1, x2]
        edge_y = [y1, y2]
        plt.plot(edge_x, edge_y, color='purple')
    plt.title('Overall Scenario Visualization', fontweight="bold")
    plt.xlabel('N', fontweight='bold')
    plt.ylabel('M', fontweight='bold')
    pp = PdfPages(os.path.join(image_path, graph_file_name))
    pp.savefig(UAV_topology, dpi=500, transparent=True)
    pp.savefig(UAV_guser_plot, dpi=500, transparent=True)
    pp.close()
    graph_output_dir = os.path.join(main_file_name, 'graph_output_files')
    file_num = len([name for name in os.listdir(graph_output_dir)])
    file_name = os.path.join(graph_output_dir, f'output_baseline{file_num + 1}.json')
    with open(file_name, 'w') as file_pointer:
        json.dump(UAV_location, file_pointer)


def get_user_location(parent_dir):
    """
    Function: get_user_location\n
    Parameter: parent_dir -> path of current dir\n
    Returns: Returns list of x and y coordinates of ground users\n
    """
    dir_name = 'input_files'
    file_name = 'user_input.json'
    user_input = {}
    with open(os.path.join(parent_dir, dir_name, file_name), 'r') as file_pointer:
        user_input = json.load(file_pointer)
    pos = user_input['Position of Ground users']
    x = []
    y = []
    for item in pos:
        a, b = map(float, item.split(' '))
        x.append(a)
        y.append(b)
    return (x, y)


def create_weighted_graph(placed):
    """
    Function: create_weighted_graph\n
    Parameters: placed -> list of already placed UAVs
    Returns: a weighted graph\n
    """
    global UAV_location
    UAV_G = nx.Graph()
    for node1 in placed:
        for node2 in placed:
            if node1 == node2:
                continue
            pos1 = UAV_location[node1]
            pos2 = UAV_location[node2]
            w = round(move_endpoint.movement.get_euc_dist(pos1, pos2), 2)
            UAV_G.add_edge(node1, node2, weight=w)
    return UAV_G


def add_relay_nodes(UAV_mst, placed):
    """
    Function: add_relay_nodes\n
    Parameters: UAV_mst -> UAV Euclidean MST, placed -> list of placed UAVs\n
    Functionality: Add relay nodes\n
    """
    global UAV_to_UAV_threshold, UAV_location, ground_placed, number_UAV
    threshold = int(UAV_to_UAV_threshold // cell_size)
    maxm_weight_edge_set = set()
    for (u, v, d) in UAV_mst.edges(data=True):
        if d['weight'] > threshold:
            maxm_weight_edge_set.add((u, v, d['weight']))
    for edge in maxm_weight_edge_set:
        u, v, weight = edge
        number_of_relay_nodes = int(weight // threshold)
        pos1 = UAV_location[u]
        pos2 = UAV_location[v]
        if pos1 > pos2:
            pos2, pos1 = pos1, pos2
        x1, y1 = pos1
        x2, y2 = pos2
        for i in range(1, number_of_relay_nodes + 1):
            UAV_node = placed[-1] + 1
            if UAV_node > number_UAV:
                write_output(placed)
                return
            req_dist = (((i * threshold) - 1) / weight)
            x = x1 + req_dist * (x2 - x1)
            y = y1 + req_dist * (y2 - y1)
            loc = (int(x), int(y))
            UAV_location[UAV_node] = loc
            placed.append(UAV_node)
            print(f'Added Relay Node {UAV_node} at {loc}')
            user_list = users_endpoint.users.get_users_cell_connections(loc)
            for user in user_list:
                ground_placed.append(user)
            if done_simulation(ground_placed, placed):
                break
    write_output(placed)


if __name__ == "__main__":
    print(f'Initialiazing the environment')
    init()
    print(f'Initialiazed environment')
    placed = consider_user_coverage()
    weighted_graph = create_weighted_graph(placed)
    UAV_mst = nx.minimum_spanning_tree(weighted_graph)
    add_relay_nodes(UAV_mst, placed)

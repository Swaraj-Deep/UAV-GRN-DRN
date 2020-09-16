import json
import os
import random
import networkx as nx
import grn_endpoint.grn_info
import users_endpoint.users
import move_endpoint.movement
import pandas as pd

# Command python or python3

command = "python3"

# User generation Script

script = "user_secnario_producer.py"

# Maximum number of iterations

max_iter = 5

# Area Size

N = 0
M = 0

# UAV Communication threshold

UAV_to_UAV_threshold = 0

# Cell size of each subgrid

cell_size = 0

# Plot title

plot_title = ""

# Plot x label

x_label = ""

# Plot y label

y_label = ""

# Nodes to remove

nodes_rem_lst = []


def get_UAV_graph(UAV_location):
    """
    Function: get_UAV_graph\n
    Parameters: UAV_location -> list of groun users placed along with their locations\n:
    Returns: UAV graph at a particular point of time\n
    """
    global UAV_to_UAV_threshold, cell_size
    placed = [node for node, loc in UAV_location.items()]
    UAV_G = nx.Graph()
    for node in placed:
        UAV_G.add_node(node)
    for node1 in placed:
        for node2 in placed:
            if move_endpoint.movement.get_euc_dist(UAV_location[node1], UAV_location[node2]) <= int(UAV_to_UAV_threshold // cell_size) and node1 != node2:
                UAV_G.add_edge(node1, node2)
    return UAV_G


def get_motif_count(UAV_G):
    """
    Function: get_motif_count\n
    Parameters: UAV_G -> UAV graph\n
    Returns: 75% of the motif count of nodes\n
    """
    n_motif = grn_endpoint.grn_info.get_motif_dict(UAV_G)
    motifs = [motif for node, motif in n_motif.items()]
    motifs = pd.DataFrame(motifs)
    return motifs.describe()[0]['75%']


def get_network_efficiency(placed, UAV_location, UAV_G):
    """
    Function: get_network_efficiency\n
    Parameters: placed -> list of placed UAVs, UAV_location -> Dictionary of placed UAVs along with their Locations, UAV_G -> UAV_graph\n
    Returns: Network Efficiency of the network
    """
    paths = []
    for node1 in placed:
        for node2 in placed:
            if node1 != node2:
                paths.append(nx.shortest_path(UAV_G, node1, node2))
    total_edge_cost = 0
    for path in paths:
        for i in range(1, len(path)):
            pos1 = UAV_location[path[i - 1]]
            pos2 = UAV_location[path[i]]
            den = move_endpoint.movement.get_euc_dist(pos1, pos2)
            total_edge_cost += 1 / den
    n = len(placed)
    first_part = n * (n - 1)
    first_part = 1 / first_part
    return first_part * total_edge_cost


def get_connected_componets(UAV_G):
    """
    Function: get_connected_components\n
    Parameter: UAV_G -> UAV graph\n
    Returns: Number of connected components in the graph\n
    """
    return nx.number_connected_components(UAV_G)


def ground_user_coverage(UAV_location):
    """
    Function: ground_user_coverage\n
    Parameter: UAV_location -> Dictionary of placed UAVs along with their locations\n
    Reutrns: Ground users coverage percentage\n
    """
    ground_users = users_endpoint.users.get_number_ground_users()
    user_served = set()
    for node, loc in UAV_location.items():
        loc = (loc[0], loc[1])
        user_list = users_endpoint.users.get_users_cell_connections(loc)
        for user in user_list:
            user_served.add(user)
    return len(user_served) / ground_users


def parse_input_graph(file_name, dir_name):
    """
    Function: parse_input_graph\n
    Parameters: file_name -> graph_input file, dir_name -> directory of the file\n
    Returns: UAV_location dictionary and placed list\n
    """
    UAV_location = {}
    with open(os.path.join(dir_name, file_name), 'r') as file_pointer:
        UAV_location = json.load(file_pointer)
    for node, loc in UAV_location.items():
        loc = (loc[0], loc[1])
        UAV_location[node] = loc
    placed = [node for node, loc in UAV_location.items()]
    return (UAV_location, placed)
    # UAV_G = get_UAV_graph(UAV_location)
    # mc = get_motif_count(UAV_G)
    # cc = get_connected_componets(UAV_G)
    # guser = ground_user_coverage(UAV_location)
    # ne = get_network_efficiency(placed, UAV_location, UAV_G)
    # print(mc, cc, guser, ne)


def add_UAVs(x, UAV_location):
    """
    Function: add_UAVs\n
    Parameter: x -> The number of UAVs to add, UAV_location -> Current state of the UAVs\n
    Returns -> Updated State of the UAVs and placed list\n
    """
    global N, M
    placed = [node for node, loc in UAV_location.items()]
    reserved_locations = [loc for node, loc in UAV_location.items()]
    locations = []
    while len (locations) < x:
        a = random.randint(0, N)
        b = random.randint(0, M)
        if (a, b) not in reserved_locations:
            locations.append(a, b)
    for loc in locations:
        if placed[-1] + 1 not in UAV_location:
            UAV_location[placed[-1] + 1] = loc
        else:
            UAV_location[placed[-1] + 1] = loc
        placed.append(placed[-1] + 1)
    return UAV_location, placed


def remove_UAVs(x):
    """
    Function: remove_UAVs\n
    Parameter: x -> The number of UAVs to remove\n
    Functionality: remove x UAVs from the network randomly\n
    """


def process_input_graphs(file_type):
    """
    Function: process_input_graphs\n
    Parameters: None\n
    Functionality: Input the graph which is the output of Either of the algorithms i.e. main.py or baseline.py
    """
    parent_dir = os.getcwd()
    dir_name = 'graph_output_files'
    for file in os.listdir(os.path.join(parent_dir, dir_name)):
        if file_type in file:
            print(parse_input_graph(file, os.path.join(parent_dir, dir_name)))
            break


def process_baseline(x):
    """
    Function: process_baseline\n
    Parameters: x -> number of UAVs to remove\n
    Returns: For each iteration return a tuple containing motif_count, connected_components, ground_user_coverage and network efficiency
    """
    parent_dir = os.getcwd()
    dir_name = 'graph_output_files'
    os.system(f'bash fresh_analysis.sh')
    os.system(f'{command} baseline.py')
    os.system(f'bash fresh_analysis.sh')
    UAV_location, placed = parse_input_graph('output_baseline1.json', os.path.join(parent_dir, dir_name))
    UAV_G = get_UAV_graph(UAV_location)
    mc = get_motif_count(UAV_G)
    cc = get_connected_componets(UAV_G)
    guser = ground_user_coverage(UAV_location)
    ne = get_network_efficiency(placed, UAV_location, UAV_G)
    process_baseline2(x, UAV_location)
    process_baseline3(x, UAV_location)
    pass


def process_main():
    """
    Function: process_main\n
    Parameters: None\n
    Returns: For each iteration return a tuple containing motif_count, connected_components, ground_user_coverage and network efficiency
    """
    os.system(f'{command} {script}')
    os.system(f'{command} baseline.py')
    pass

def process_baseline2(x, UAV_location_baseline):
    """
    Function: process_baseline2\n
    Parameters: x -> number of UAVs to remove, UAV_location_baseline -> UAVs position in the baseline approach\n
    Returns: For each iteration return a tuple containing motif_count, connected_components, ground_user_coverage and network efficiency
    """
    parent_dir = os.getcwd()
    dir_name = 'graph_output_files'
    os.system(f'bash fresh_analysis.sh')
    os.system(f'{command} main.py')
    os.system(f'bash fresh_analysis.sh')
    UAV_location, placed = parse_input_graph('output_main1.json', os.path.join(parent_dir, dir_name))
    number_UAV_baseline = len(UAV_location_baseline)
    number_UAV_main = len(UAV_location)
    if number_UAV_baseline < number_UAV_main:
        UAV_location_baseline = add_UAVs(number_UAV_main - number_UAV_baseline, UAV_location_baseline)
    else:
        UAV_location_baseline = remove_UAVs(number_UAV_baseline - number_UAV_main, UAV_location_baseline)
    UAV_G = get_UAV_graph(UAV_location_baseline)
    mc = get_motif_count(UAV_G)
    cc = get_connected_componets(UAV_G)
    guser = ground_user_coverage(UAV_location_baseline)
    ne = get_network_efficiency(placed, UAV_location_baseline, UAV_G)
    pass


def process_baseline3():
    """
    Function: process_baseline3\n
    Parameters: None\n
    Returns: For each iteration return a tuple containing motif_count, connected_components, ground_user_coverage and network efficiency
    """
    print("Bye")
    pass
   
   


def simulate_plot_making():
    """
    Function: simulate_plot_making\n
    Parameter: None\n
    Functionality: Simulate the plot making process\n
    """
    global nodes_rem_lst
    baseline_lst = []
    main_lst = []
    baseline2_lst = []
    baseline3_lst = []
    for x in nodes_rem_lst:
        for _ in range(max_iter):
            os.system(f'{command} {script}')
            baseline_lst.append(process_baseline())
        for _ in range(max_iter):
            main_lst.append(process_main())



def init():
    """
    Function: init
    Functionality: Sets all the global variables
    """
    global UAV_to_UAV_threshold, cell_size, plot_title, x_label, y_label, nodes_rem_lst, N, M
    parent_dir = os.getcwd()
    parent_dir = os.getcwd()
    folder_name = 'input_files'
    file_name = 'scenario_input.json'
    file_path = os.path.join(parent_dir, folder_name, file_name)
    with open(file_path, 'r') as file_pointer:
        file_data = json.load(file_pointer)
        UAV_to_UAV_threshold = file_data['UAV_to_UAV_threshold']
        cell_size = file_data['cell_size']
        unit_mul = file_data['unit_multiplier']
        N = file_data['N']
        M = file_data['M']
    UAV_to_UAV_threshold *= unit_mul
    cell_size *= unit_mul
    file_name = 'new_plot.json'
    file_path = os.path.join(parent_dir, folder_name, file_name)
    with open(file_path, 'r') as file_pointer:
        file_data = json.load(file_pointer)
        plot_title = file_data['Plot title']
        x_label = file_data['x-label']
        y_label = file_data['y-label']
        nodes_rem_lst = file_data['Nodes']
    users_endpoint.users.init()
    grn_endpoint.grn_info.init()
    process_input_graphs('main40')


if __name__ == "__main__":
    init()

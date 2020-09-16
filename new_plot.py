import json
import os
import random
import networkx as nx
import grn_endpoint.grn_info
import users_endpoint.users
import move_endpoint.movement
import pandas as pd
import matplotlib.pyplot as plt

# Command python or python3

command = "python3"

# User generation Script

script = "user_secnario_producer.py"

# Maximum number of iterations

max_iter = 1

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
                try:
                    paths.append(nx.shortest_path(UAV_G, node1, node2))
                except Exception as ex:
                    pass
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
    UAV_loc = {}
    for node, loc in UAV_location.items():
        UAV_loc[int(node)] = (loc[0], loc[1])
    placed = [node for node in UAV_loc]
    return (UAV_loc, placed)


def add_UAVs(x, UAV_loc):
    """
    Function: add_UAVs\n
    Parameter: x -> The number of UAVs to add, UAV_loc -> Current state of the UAVs\n
    Returns -> Updated State of the UAVs and placed list\n
    """
    global N, M
    UAV_location = {}
    for node, loc in UAV_loc.items():
        UAV_location[node] = loc
    placed = [node for node, loc in UAV_location.items()]
    reserved_locations = [loc for node, loc in UAV_location.items()]
    locations = []
    while len(locations) < x:
        a = random.randint(0, N)
        b = random.randint(0, M)
        if (a, b) not in reserved_locations:
            locations.append((a, b))
    for loc in locations:
        key = int(placed[-1]) + 1
        if key not in UAV_location:
            UAV_location[key] = loc
        else:
            UAV_location[key] = loc
        placed.append(key)
    placed = [node for node, loc in UAV_location.items()]
    return UAV_location, placed


def remove_UAVs(x, UAV_loc):
    """
    Function: remove_UAVs\n
    Parameter: x -> The number of UAVs to remove, UAV_loc -> Scenario of UAVs to remove\n
    Functionality: remove x UAVs from the network randomly\n
    """
    UAV_location = {}
    for node, loc in UAV_loc.items():
        UAV_location[node] = loc
    len_old = len(UAV_location)
    diff = len_old - x
    if diff < 0:
        diff = 0
    while len(UAV_location) > diff:
        placed = [node for node, loc in UAV_location.items()]
        rem = placed[random.randint(0, len(placed) - 1)]
        UAV_location.pop(rem)
    placed = [node for node, loc in UAV_location.items()]
    return UAV_location, placed


def process_baseline2(UAV_location_main, UAV_location_baseline):
    """
    Function: process_baseline2\n
    Parameters: UAV_location_main -> UAVs position in the main approach, UAV_location_baseline -> UAVs position in the baseline approach\n
    Returns: Modified UAV_location and placed list\n
    """
    len_main = len(UAV_location_main)
    len_baseline = len(UAV_location_baseline)
    if len_main > len_baseline:
        return add_UAVs(len_main - len_baseline, UAV_location_baseline)
    else:
        return remove_UAVs(len_baseline - len_main, UAV_location_baseline)


def process_baseline3(UAV_location_main, UAV_location_baseline):
    """
    Function: process_baseline3\n
    Parameters: UAV_location_main -> UAVs position in the main approach, UAV_location_baseline -> UAVs position in the baseline approach\n
    Returns: Modified UAV_location and placed list\n
    """
    len_main = len(UAV_location_main)
    len_baseline = len(UAV_location_baseline)
    if len_baseline >= int(1.5 * len_main):
        return remove_UAVs(len_baseline - (1.5 * len_main), UAV_location_baseline)
    else:
        return add_UAVs((1.5 * len_main) - len_baseline, UAV_location_baseline)


def run(x):
    """
    Function: run\n
    Parameter: x -> Number of UAVs to delete\n
    Functionality: Runs all the four simulations\n
    """
    parent_dir = os.getcwd()
    dir_name = 'graph_output_files'
    os.system(f'bash fresh_analysis.sh')
    os.system(f'{command} baseline.py')
    os.system(f'{command} main.py')
    UAV_location_baseline, placed = parse_input_graph(
        'output_baseline1.json', os.path.join(parent_dir, dir_name))
    UAV_location, placed = remove_UAVs(x, UAV_location_baseline)
    UAV_G = get_UAV_graph(UAV_location)
    mc = get_motif_count(UAV_G)
    cc = get_connected_componets(UAV_G)
    guser = ground_user_coverage(UAV_location)
    ne = get_network_efficiency(placed, UAV_location, UAV_G)
    ret_val1 = (mc, cc, guser, ne)
    UAV_location_main, placed = parse_input_graph(
        'output_main2.json', os.path.join(parent_dir, dir_name))
    UAV_location, placed = remove_UAVs(x, UAV_location_main)
    UAV_G = get_UAV_graph(UAV_location)
    mc = get_motif_count(UAV_G)
    cc = get_connected_componets(UAV_G)
    guser = ground_user_coverage(UAV_location)
    ne = get_network_efficiency(placed, UAV_location, UAV_G)
    ret_val2 = (mc, cc, guser, ne)
    UAV_location_baseline2, placed = process_baseline2(
        UAV_location_main, UAV_location_baseline)
    UAV_location, placed = remove_UAVs(x, UAV_location_baseline2)
    UAV_G = get_UAV_graph(UAV_location)
    mc = get_motif_count(UAV_G)
    cc = get_connected_componets(UAV_G)
    guser = ground_user_coverage(UAV_location)
    ne = get_network_efficiency(placed, UAV_location, UAV_G)
    ret_val3 = (mc, cc, guser, ne)
    UAV_location_baseline3, placed = process_baseline3(
        UAV_location_main, UAV_location_baseline)
    UAV_location, placed = remove_UAVs(x, UAV_location_baseline3)
    UAV_G = get_UAV_graph(UAV_location)
    mc = get_motif_count(UAV_G)
    cc = get_connected_componets(UAV_G)
    guser = ground_user_coverage(UAV_location)
    ne = get_network_efficiency(placed, UAV_location, UAV_G)
    ret_val4 = (mc, cc, guser, ne)
    os.system(f'bash fresh_analysis.sh')
    return (ret_val1, ret_val2, ret_val3, ret_val4)


def process_output(baseline_dict, main_dict, baseline2_dict, baseline3_dict):
    """
    Function: process_output\n
    Parameters: baseline_dict -> output of baseline, main_dict -> output of main, baseline2_dict -> output of baseline2, baseline3_dict -> output of baseline3
    """
    for x, ret_val_lst in baseline_dict.items():
        mc = []
        cc = []
        guser = []
        ne = []
        for ret_val in ret_val_lst:
            m, c, g, n = ret_val
            mc.append(m)
            cc.append(c)
            guser.append(g)
            ne.append(n)
        baseline_dict[x] = [(pd.DataFrame(mc).describe()[0]['mean'], pd.DataFrame(cc).describe()[
                             0]['75%'], pd.DataFrame(guser).describe()[0]['75%'], pd.DataFrame(ne).describe()[0]['75%'])]
    for x, ret_val_lst in main_dict.items():
        mc = []
        cc = []
        guser = []
        ne = []
        for ret_val in ret_val_lst:
            m, c, g, n = ret_val
            mc.append(m)
            cc.append(c)
            guser.append(g)
            ne.append(n)
        main_dict[x] = [(pd.DataFrame(mc).describe()[0]['mean'], pd.DataFrame(cc).describe()[
                         0]['75%'], pd.DataFrame(guser).describe()[0]['75%'], pd.DataFrame(ne).describe()[0]['75%'])]
    for x, ret_val_lst in baseline2_dict.items():
        mc = []
        cc = []
        guser = []
        ne = []
        for ret_val in ret_val_lst:
            m, c, g, n = ret_val
            mc.append(m)
            cc.append(c)
            guser.append(g)
            ne.append(n)
        baseline2_dict[x] = [(pd.DataFrame(mc).describe()[0]['mean'], pd.DataFrame(cc).describe()[
                              0]['75%'], pd.DataFrame(guser).describe()[0]['75%'], pd.DataFrame(ne).describe()[0]['75%'])]
    for x, ret_val_lst in baseline3_dict.items():
        mc = []
        cc = []
        guser = []
        ne = []
        for ret_val in ret_val_lst:
            m, c, g, n = ret_val
            mc.append(m)
            cc.append(c)
            guser.append(g)
            ne.append(n)
        baseline3_dict[x] = [(pd.DataFrame(mc).describe()[0]['mean'], pd.DataFrame(cc).describe()[
                              0]['75%'], pd.DataFrame(guser).describe()[0]['75%'], pd.DataFrame(ne).describe()[0]['75%'])]
    draw_plot(baseline_dict, main_dict, baseline2_dict, baseline3_dict)


def draw_plot(baseline_dict, main_dict, baseline2_dict, baseline3_dict):
    """
    Function: draw_plot\n
    Parameters: baseline_dict -> Processed values of baseline_dict, main_dict -> Processed values of main_dict, baseline2_dict -> Processed values of baseline2_dict, baseline3_dict -> Processed values of baseline3_dict\n
    Functionality: Draws the plot\n
    """
    global plot_title, x_label, y_label
    overall_dict = {
        "Baseline": baseline_dict,
        "Main": main_dict,
        "Baseline2": baseline2_dict,
        "Baseline3": baseline3_dict
    }
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    with open(os.path.join(parent_dir, dir_name, 'new_plot_output.json'), 'w') as file_pointer:
        json.dump(overall_dict, file_pointer)
    # x_axis = [x for x, ret_val in baseline_dict.items()]
    # y_data = [ret_val[0] for x, ret_val in baseline_dict.items()]
    # print(x_axis, y_data)
    # for xpts, ypts in zip(x_axis, y_data):
    #     plt.scatter([xpts] * len(ypts), ypts, label=f'Baseline')
    # plt.xticks(x_axis)
    # plt.axes().set_xticklabels(x_axis)
    # x_axis = [x for x, ret_val in main_dict.items()]
    # y_data = [ret_val[0] for x, ret_val in main_dict.items()]
    # for xpts, ypts in zip(x_axis, y_data):
    #     plt.scatter([xpts] * len(ypts), ypts, label=f'Main')
    # plt.xticks(x_axis)
    # plt.axes().set_xticklabels(x_axis)
    # x_axis = [x for x, ret_val in baseline2_dict.items()]
    # y_data = [ret_val[0] for x, ret_val in baseline2_dict.items()]
    # for xpts, ypts in zip(x_axis, y_data):
    #     plt.scatter([xpts] * len(ypts), ypts, label=f'Baseline2')
    # plt.xticks(x_axis)
    # plt.axes().set_xticklabels(x_axis)
    # x_axis = [x for x, ret_val in baseline3_dict.items()]
    # y_data = [ret_val[0] for x, ret_val in baseline3_dict.items()]
    # for xpts, ypts in zip(x_axis, y_data):
    #     plt.scatter([xpts] * len(ypts), ypts, label=f'Baseline3')
    # plt.xticks(x_axis)
    # plt.axes().set_xticklabels(x_axis)
    # plt.title(
    #     plot_title, fontweight="bold")
    # plt.xlabel(x_label, fontweight='bold')
    # plt.ylabel(y_label, fontweight='bold')
    # plt.legend()
    # plt.show()


def simulate_plot_making():
    """
    Function: simulate_plot_making\n
    Parameter: None\n
    Functionality: Simulate the plot making process\n
    """
    global nodes_rem_lst
    baseline_dict = {}
    main_dict = {}
    baseline2_dict = {}
    baseline3_dict = {}
    for x in nodes_rem_lst:
        for _ in range(max_iter):
            os.system(f'{command} {script}')
            r1, r2, r3, r4 = run(x)
            if x not in baseline_dict:
                baseline_dict[x] = [r1]
            else:
                baseline_dict[x].append(r1)
            if x not in main_dict:
                main_dict[x] = [r2]
            else:
                main_dict[x].append(r2)
            if x not in baseline2_dict:
                baseline2_dict[x] = [r3]
            else:
                baseline2_dict[x].append(r3)
            if x not in baseline3_dict:
                baseline3_dict[x] = [r4]
            else:
                baseline3_dict[x].append(r4)
    process_output(baseline_dict, main_dict, baseline2_dict, baseline3_dict)


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
    simulate_plot_making()


if __name__ == "__main__":
    print(f'Relax!! we have taken the charge. (-_-)')
    init()

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

# Nodes to remove

nodes_rem_lst = []


# Flag variable

flag = True

# Global dictionaries

UAV_location_clone = {}
UAV_location_clone1 = {}
UAV_location_main = {}
UAV_location_baseline = {}

# Global Count Variables

nodes_main = 0
nodes_baseline = 0
nodes_baseline2 = 0
nodes_baseline3 = 0


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
    Returns: mean of the motif count of nodes\n
    """
    return sum(nx.triangles(UAV_G).values()) / 3


def get_network_efficiency(placed, UAV_location, UAV_G):
    """
    Function: get_network_efficiency\n
    Parameters: placed -> list of placed UAVs, UAV_location -> Dictionary of placed UAVs along with their Locations, UAV_G -> UAV_graph\n
    Returns: Network Efficiency of the network
    """
    return nx.global_efficiency(UAV_G)


def get_connected_componets(UAV_G):
    """
    Function: get_connected_components\n
    Parameter: UAV_G -> UAV graph\n
    Returns: Number of connected components in the graph\n
    """
    return nx.number_connected_components(UAV_G)


def no_nodes_in_largest_connected_component(UAV_G):
    """
    Function: no_nodes_in_largest_connected_component\n
    Parameter: UAV_G -> UAV graph\n
    Returns: Number of nodes in the largest connected components in the graph\n
    """
    len_cc = [len(UAV_G.subgraph(c)) for c in nx.connected_components(UAV_G)]
    if len_cc:
        return max(len_cc)
    else:
        return 0


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


def remove_UAVs(x, UAV_location):
    """
    Function: remove_UAVs\n
    Parameter: x -> The number of UAVs to remove, UAV_location -> Scenario of UAVs to remove\n
    Functionality: remove x UAVs from the network randomly\n
    """
    len_old = len(UAV_location)
    diff = len_old - x
    if diff < 0:
        diff = 0
    while len(UAV_location) > diff:
        UAV_G = get_UAV_graph(UAV_location)
        deg_lst = list(UAV_G.degree())
        deg_lst.sort(key=lambda x: x[1], reverse=True)
        rem, degree = deg_lst[0]
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


def run(i):
    """
    Function: run\n
    Parameter: i -> index of the precentage to delete\n
    Functionality: Runs all the four simulations\n
    """
    global flag, nodes_rem_lst, nodes_baseline, nodes_main, nodes_baseline2, nodes_baseline3
    global UAV_location_clone, UAV_location_clone1, UAV_location_baseline, UAV_location_main
    parent_dir = os.getcwd()
    dir_name = 'graph_output_files'
    if flag:
        UAV_location_baseline, placed = parse_input_graph(
            'output_baseline1.json', os.path.join(parent_dir, dir_name))
        nodes_baseline = len(UAV_location_baseline)
        for node, loc in UAV_location_baseline.items():
            UAV_location_clone[node] = loc
            UAV_location_clone1[node] = loc
    if i == 0:
        x = int(nodes_baseline * nodes_rem_lst[i])
        UAV_location, placed = remove_UAVs(x, UAV_location_baseline)
    else:
        y = int(nodes_baseline * nodes_rem_lst[i - 1])
        x = int(nodes_baseline * nodes_rem_lst[i])
        x = abs(x - y)
        UAV_location, placed = remove_UAVs(x, UAV_location_baseline)
    UAV_G = get_UAV_graph(UAV_location)
    mx = no_nodes_in_largest_connected_component(UAV_G)
    mc = get_motif_count(UAV_G)
    cc = get_connected_componets(UAV_G)
    guser = ground_user_coverage(UAV_location)
    ne = get_network_efficiency(placed, UAV_location, UAV_G)
    ret_val1 = (mc, cc, guser, ne, mx)
    ax = plt.gca()
    ax.set_title(f'{nodes_rem_lst[i] * 100} Baseline Approach')
    nx.draw(UAV_G, with_labels=True, ax=ax)
    _ = ax.axis('off')   
    plt.show()
    if flag:
        UAV_location_main, placed = parse_input_graph(
            'output_main2.json', os.path.join(parent_dir, dir_name))
        nodes_main = len(UAV_location_main)
        nodes_baseline2 = nodes_main
        nodes_baseline3 = int(nodes_main * 1.5)
        flag = False
    if i == 0:
        x = int(nodes_main * nodes_rem_lst[i])
        UAV_location, placed = remove_UAVs(x, UAV_location_main)
    else:
        y = int(nodes_main * nodes_rem_lst[i - 1])
        x = int(nodes_main * nodes_rem_lst[i])
        x = abs(x - y)
        UAV_location, placed = remove_UAVs(x, UAV_location_main)
    UAV_G = get_UAV_graph(UAV_location)
    mx = no_nodes_in_largest_connected_component(UAV_G)
    mc = get_motif_count(UAV_G)
    cc = get_connected_componets(UAV_G)
    guser = ground_user_coverage(UAV_location)
    ne = get_network_efficiency(placed, UAV_location, UAV_G)
    ret_val2 = (mc, cc, guser, ne, mx)
    ax = plt.gca()
    ax.set_title(f'{nodes_rem_lst[i] * 100} Main Approach')
    nx.draw(UAV_G, with_labels=True, ax=ax)
    _ = ax.axis('off')   
    plt.show()
    if i == 0:
        x = int(nodes_baseline2 * nodes_rem_lst[i])
        UAV_location_baseline2, placed = process_baseline2(
            UAV_location_main, UAV_location_clone)
        UAV_location, placed = remove_UAVs(x, UAV_location_baseline2)
    else:
        y = int(nodes_baseline2 * nodes_rem_lst[i - 1])
        x = int(nodes_baseline2 * nodes_rem_lst[i])
        x = abs(x - y)
        UAV_location_baseline2, placed = process_baseline2(
            UAV_location_main, UAV_location_clone)
        UAV_location, placed = remove_UAVs(x, UAV_location_baseline2)
    UAV_G = get_UAV_graph(UAV_location)
    mc = get_motif_count(UAV_G)
    mx = no_nodes_in_largest_connected_component(UAV_G)
    cc = get_connected_componets(UAV_G)
    guser = ground_user_coverage(UAV_location)
    ne = get_network_efficiency(placed, UAV_location, UAV_G)
    ret_val3 = (mc, cc, guser, ne, mx)
    ax = plt.gca()
    ax.set_title(f'{nodes_rem_lst[i] * 100} Baseline2 Approach')
    nx.draw(UAV_G, with_labels=True, ax=ax)
    _ = ax.axis('off')   
    plt.show()
    if i == 0:
        x = int(nodes_baseline3 * nodes_rem_lst[i])
        UAV_location_baseline3, placed = process_baseline3(
            UAV_location_main, UAV_location_clone1)
        UAV_location, placed = remove_UAVs(x, UAV_location_baseline3)
    else:
        y = int(nodes_baseline3 * nodes_rem_lst[i - 1])
        x = int(nodes_baseline3 * nodes_rem_lst[i])
        x = abs(x - y)
        UAV_location_baseline3, placed = process_baseline3(
            UAV_location_main, UAV_location_clone1)
        UAV_location, placed = remove_UAVs(x, UAV_location_baseline3)
    UAV_G = get_UAV_graph(UAV_location)
    mc = get_motif_count(UAV_G)
    mx = no_nodes_in_largest_connected_component(UAV_G)
    cc = get_connected_componets(UAV_G)
    guser = ground_user_coverage(UAV_location)
    ne = get_network_efficiency(placed, UAV_location, UAV_G)
    ret_val4 = (mc, cc, guser, ne, mx)
    ax = plt.gca()
    ax.set_title(f'{nodes_rem_lst[i] * 100} Baseline3 Approach')
    nx.draw(UAV_G, with_labels=True, ax=ax)
    _ = ax.axis('off')   
    plt.show()
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
        mx = []
        for ret_val in ret_val_lst:
            m, c, g, n, l = ret_val
            mc.append(m)
            cc.append(c)
            guser.append(g)
            ne.append(n)
            mx.append(l)
        baseline_dict[x] = [([pd.DataFrame(mc).describe()[0]['mean'], pd.DataFrame(mc).describe()[0]['75%'], pd.DataFrame(mc).describe()[0]['std'], pd.DataFrame(mc).describe()[0]['50%']], [pd.DataFrame(cc).describe()[
                             0]['75%'], pd.DataFrame(cc).describe()[
            0]['mean'], pd.DataFrame(cc).describe()[
            0]['50%'], pd.DataFrame(cc).describe()[
            0]['std']], [pd.DataFrame(guser).describe()[0]['75%'], pd.DataFrame(guser).describe()[0]['mean'], pd.DataFrame(guser).describe()[0]['50%'], pd.DataFrame(guser).describe()[0]['std']], [pd.DataFrame(ne).describe()[0]['75%'], pd.DataFrame(ne).describe()[0]['mean'], pd.DataFrame(ne).describe()[0]['50%'], pd.DataFrame(ne).describe()[0]['std']], [pd.DataFrame(mx).describe()[
                0]['75%'], pd.DataFrame(mx).describe()[
                0]['mean'], pd.DataFrame(mx).describe()[
                0]['50%'], pd.DataFrame(mx).describe()[
                0]['std']])]
    for x, ret_val_lst in main_dict.items():
        mc = []
        cc = []
        guser = []
        ne = []
        mx = []
        for ret_val in ret_val_lst:
            m, c, g, n, l = ret_val
            mc.append(m)
            cc.append(c)
            guser.append(g)
            ne.append(n)
            mx.append(l)
        main_dict[x] = [([pd.DataFrame(mc).describe()[0]['mean'], pd.DataFrame(mc).describe()[0]['75%'], pd.DataFrame(mc).describe()[0]['std'], pd.DataFrame(mc).describe()[0]['50%']], [pd.DataFrame(cc).describe()[
            0]['75%'], pd.DataFrame(cc).describe()[
            0]['mean'], pd.DataFrame(cc).describe()[
            0]['50%'], pd.DataFrame(cc).describe()[
            0]['std']], [pd.DataFrame(guser).describe()[0]['75%'], pd.DataFrame(guser).describe()[0]['mean'], pd.DataFrame(guser).describe()[0]['50%'], pd.DataFrame(guser).describe()[0]['std']], [pd.DataFrame(ne).describe()[0]['75%'], pd.DataFrame(ne).describe()[0]['mean'], pd.DataFrame(ne).describe()[0]['50%'], pd.DataFrame(ne).describe()[0]['std']], [pd.DataFrame(mx).describe()[
                0]['75%'], pd.DataFrame(mx).describe()[
                0]['mean'], pd.DataFrame(mx).describe()[
                0]['50%'], pd.DataFrame(mx).describe()[
                0]['std']])]
    for x, ret_val_lst in baseline2_dict.items():
        mc = []
        cc = []
        guser = []
        ne = []
        mx = []
        for ret_val in ret_val_lst:
            m, c, g, n, l = ret_val
            mc.append(m)
            cc.append(c)
            guser.append(g)
            ne.append(n)
            mx.append(l)
        baseline2_dict[x] = [([pd.DataFrame(mc).describe()[0]['mean'], pd.DataFrame(mc).describe()[0]['75%'], pd.DataFrame(mc).describe()[0]['std'], pd.DataFrame(mc).describe()[0]['50%']], [pd.DataFrame(cc).describe()[
                             0]['75%'], pd.DataFrame(cc).describe()[
            0]['mean'], pd.DataFrame(cc).describe()[
            0]['50%'], pd.DataFrame(cc).describe()[
            0]['std']], [pd.DataFrame(guser).describe()[0]['75%'], pd.DataFrame(guser).describe()[0]['mean'], pd.DataFrame(guser).describe()[0]['50%'], pd.DataFrame(guser).describe()[0]['std']], [pd.DataFrame(ne).describe()[0]['75%'], pd.DataFrame(ne).describe()[0]['mean'], pd.DataFrame(ne).describe()[0]['50%'], pd.DataFrame(ne).describe()[0]['std']], [pd.DataFrame(mx).describe()[
                0]['75%'], pd.DataFrame(mx).describe()[
                0]['mean'], pd.DataFrame(mx).describe()[
                0]['50%'], pd.DataFrame(mx).describe()[
                0]['std']])]
    for x, ret_val_lst in baseline3_dict.items():
        mc = []
        cc = []
        guser = []
        ne = []
        mx = []
        for ret_val in ret_val_lst:
            m, c, g, n, l = ret_val
            mc.append(m)
            cc.append(c)
            guser.append(g)
            ne.append(n)
            mx.append(l)
        baseline3_dict[x] = [([pd.DataFrame(mc).describe()[0]['mean'], pd.DataFrame(mc).describe()[0]['75%'], pd.DataFrame(mc).describe()[0]['std'], pd.DataFrame(mc).describe()[0]['50%']], [pd.DataFrame(cc).describe()[
                             0]['75%'], pd.DataFrame(cc).describe()[
            0]['mean'], pd.DataFrame(cc).describe()[
            0]['50%'], pd.DataFrame(cc).describe()[
            0]['std']], [pd.DataFrame(guser).describe()[0]['75%'], pd.DataFrame(guser).describe()[0]['mean'], pd.DataFrame(guser).describe()[0]['50%'], pd.DataFrame(guser).describe()[0]['std']], [pd.DataFrame(ne).describe()[0]['75%'], pd.DataFrame(ne).describe()[0]['mean'], pd.DataFrame(ne).describe()[0]['50%'], pd.DataFrame(ne).describe()[0]['std']], [pd.DataFrame(mx).describe()[
                0]['75%'], pd.DataFrame(mx).describe()[
                0]['mean'], pd.DataFrame(mx).describe()[
                0]['50%'], pd.DataFrame(mx).describe()[
                0]['std']])]
    draw_plot(baseline_dict, main_dict, baseline2_dict, baseline3_dict)


def draw_plot(baseline_dict, main_dict, baseline2_dict, baseline3_dict):
    """
    Function: draw_plot\n
    Parameters: baseline_dict -> Processed values of baseline_dict, main_dict -> Processed values of main_dict, baseline2_dict -> Processed values of baseline2_dict, baseline3_dict -> Processed values of baseline3_dict\n
    Functionality: Draws the plot\n
    """
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
    x_axis = [x for x, ret_val in baseline_dict.items()]
    b_mc_y = []
    m_mc_y = []
    b2_mc_y = []
    b3_mc_y = []
    for x in baseline_dict:
        b_mc_y.append(baseline_dict[x][0][0][0])
        m_mc_y.append(main_dict[x][0][0][0])
        b2_mc_y.append(baseline2_dict[x][0][0][0])
        b3_mc_y.append(baseline3_dict[x][0][0][0])
    plt.scatter(x_axis, b_mc_y)
    plt.plot(x_axis, b_mc_y, label=f'Baseline')
    plt.scatter(x_axis, m_mc_y)
    plt.plot(x_axis, m_mc_y, label=f'Main')
    plt.scatter(x_axis, b2_mc_y)
    plt.plot(x_axis, b2_mc_y, label=f'Baseline2')
    plt.scatter(x_axis, b3_mc_y)
    plt.plot(x_axis, b3_mc_y, label=f'Baseline3')
    plt.legend()
    plt.title('Motif Count Vs Number of UAV Removed', fontweight="bold")
    plt.xlabel('Number of UAV to remove', fontweight='bold')
    plt.ylabel('Average Motif Count', fontweight='bold')
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'MotifvsUAVremoved'
    plt.savefig(os.path.join(parent_dir, dir_name, file_name))
    plt.clf()
    b_cc_y = []
    m_cc_y = []
    b2_cc_y = []
    b3_cc_y = []
    for x in baseline_dict:
        b_cc_y.append(baseline_dict[x][0][1][0])
        m_cc_y.append(main_dict[x][0][1][0])
        b2_cc_y.append(baseline2_dict[x][0][1][0])
        b3_cc_y.append(baseline3_dict[x][0][1][0])
    plt.scatter(x_axis, b_cc_y)
    plt.plot(x_axis, b_cc_y, label=f'Baseline')
    plt.scatter(x_axis, m_cc_y)
    plt.plot(x_axis, m_cc_y, label=f'Main')
    plt.scatter(x_axis, b2_cc_y)
    plt.plot(x_axis, b2_cc_y, label=f'Baseline2')
    plt.scatter(x_axis, b3_cc_y)
    plt.plot(x_axis, b3_cc_y, label=f'Baseline3')
    plt.legend()
    plt.title('Connected Components Vs Number of UAV Removed', fontweight="bold")
    plt.xlabel('Number of UAV to remove', fontweight='bold')
    plt.ylabel('Number of Connected Components', fontweight='bold')
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'ConnectedvsUAVremoved'
    plt.savefig(os.path.join(parent_dir, dir_name, file_name))
    plt.clf()
    b_gu_y = []
    m_gu_y = []
    b2_gu_y = []
    b3_gu_y = []
    for x in baseline_dict:
        b_gu_y.append(baseline_dict[x][0][2][0])
        m_gu_y.append(main_dict[x][0][2][0])
        b2_gu_y.append(baseline2_dict[x][0][2][0])
        b3_gu_y.append(baseline3_dict[x][0][2][0])
    plt.scatter(x_axis, b_gu_y)
    plt.plot(x_axis, b_gu_y, label=f'Baseline')
    plt.scatter(x_axis, m_gu_y)
    plt.plot(x_axis, m_gu_y, label=f'Main')
    plt.scatter(x_axis, b2_gu_y)
    plt.plot(x_axis, b2_gu_y, label=f'Baseline2')
    plt.scatter(x_axis, b3_gu_y)
    plt.plot(x_axis, b3_gu_y, label=f'Baseline3')
    plt.legend()
    plt.title('Ground User percentage Vs Number of UAV Removed',
              fontweight="bold")
    plt.xlabel('Number of UAV to remove', fontweight='bold')
    plt.ylabel('Ground User percentage', fontweight='bold')
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'Ground_user_coveragevsUAVremoved'
    plt.savefig(os.path.join(parent_dir, dir_name, file_name))
    plt.clf()
    b_ne_y = []
    m_ne_y = []
    b2_ne_y = []
    b3_ne_y = []
    for x in baseline_dict:
        b_ne_y.append(baseline_dict[x][0][3][0])
        m_ne_y.append(main_dict[x][0][3][0])
        b2_ne_y.append(baseline2_dict[x][0][3][0])
        b3_ne_y.append(baseline3_dict[x][0][3][0])
    plt.scatter(x_axis, b_ne_y)
    plt.plot(x_axis, b_ne_y, label=f'Baseline')
    plt.scatter(x_axis, m_ne_y)
    plt.plot(x_axis, m_ne_y, label=f'Main')
    plt.scatter(x_axis, b2_ne_y)
    plt.plot(x_axis, b2_ne_y, label=f'Baseline2')
    plt.scatter(x_axis, b3_ne_y)
    plt.plot(x_axis, b3_ne_y, label=f'Baseline3')
    plt.legend()
    plt.title('Network Efficiency Vs Number of UAV Removed', fontweight="bold")
    plt.xlabel('Number of UAV to remove', fontweight='bold')
    plt.ylabel('Network Efficiency', fontweight='bold')
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'NetworkEfficiencyvsUAVremoved'
    plt.savefig(os.path.join(parent_dir, dir_name, file_name))
    plt.clf()
    b_mx_y = []
    m_mx_y = []
    b2_mx_y = []
    b3_mx_y = []
    for x in baseline_dict:
        b_mx_y.append(baseline_dict[x][0][4][0])
        m_mx_y.append(main_dict[x][0][4][0])
        b2_mx_y.append(baseline2_dict[x][0][4][0])
        b3_mx_y.append(baseline3_dict[x][0][4][0])
    plt.scatter(x_axis, b_mx_y)
    plt.plot(x_axis, b_mx_y, label=f'Baseline')
    plt.scatter(x_axis, m_mx_y)
    plt.plot(x_axis, m_mx_y, label=f'Main')
    plt.scatter(x_axis, b2_mx_y)
    plt.plot(x_axis, b2_mx_y, label=f'Baseline2')
    plt.scatter(x_axis, b3_mx_y)
    plt.plot(x_axis, b3_mx_y, label=f'Baseline3')
    plt.legend()
    plt.title('Nodes in largest connected component Vs Number of UAV Removed', fontweight="bold")
    plt.xlabel('Number of UAV to remove', fontweight='bold')
    plt.ylabel('Node in largest connected component', fontweight='bold')
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'NodeslargestccvsUAVremoved'
    plt.savefig(os.path.join(parent_dir, dir_name, file_name))
    plt.clf()


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
    global flag
    global UAV_location_clone, UAV_location_clone1, UAV_location_main, UAV_location_baseline
    for _ in range(max_iter):
        os.system(f'bash fresh_analysis.sh')
        os.system(f'{command} {script}')
        os.system(f'{command} baseline.py')
        os.system(f'{command} main.py')
        flag = True
        UAV_location_clone = {}
        UAV_location_clone1 = {}
        UAV_location_baseline = {}
        UAV_location_main = {}
        for i in range(len(nodes_rem_lst)):
            x = nodes_rem_lst[i]
            r1, r2, r3, r4 = run(i)
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
    global UAV_to_UAV_threshold, cell_size, nodes_rem_lst, N, M
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
        nodes_rem_lst = file_data['Nodes']
    users_endpoint.users.init()
    grn_endpoint.grn_info.init()
    simulate_plot_making()


if __name__ == "__main__":
    dir_path = os.path.join(os.getcwd(), 'analysis_output_files')
    try:
        os.mkdir(dir_path)
    except OSError as error:
        pass
    print(f'Relax!! we have taken the charge. (-_-)')
    init()

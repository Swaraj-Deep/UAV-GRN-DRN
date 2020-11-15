import os
import json
import grn_endpoint.grn_info
import move_endpoint.movement
import numpy as np
import collections
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

command = "python3"
script = "user_secnario_producer.py"
UAV_to_UAV_threshold = 0
cell_size = 0


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


def init():
    """
    Function: init\n
    Parameter: None\n
    Functionality: Initialiazes the GRN environment\n
    """
    grn_endpoint.grn_info.init()
    degree_data = get_degree_count()
    motif_data = get_motif_count()
    return (degree_data, motif_data)


def get_degree_count():
    """
    Function: get_degree_count\n
    Parameter: None\n
    Returns: dictionary containing key as degree and value as number of nodes having that degree\n
    """
    degrees_val = sorted([degree for node,
                          degree in grn_endpoint.grn_info.get_grn_graph().degree()])
    degrees_count = dict(collections.Counter(degrees_val))
    return degrees_count


def get_motif_count():
    """
    Function: get_motif_count\n
    Parameter: None\n
    Returns: dictionary containing key as motif and value as number of nodes having that motif\n
    """
    motifs_val = sorted([motif for node, motif in dict(
        grn_endpoint.grn_info.get_n_motif()).items()])
    motifs_count = dict(collections.Counter(motifs_val))
    return motifs_count


def write_to_json(data, file_path):
    """
    Function: write_to_json\n
    Parameters: data -> data to be written, file_path -> path of the file\n
    Functionality: Writes the json data to the file\n
    """
    with open(file_path, 'w') as file_pointer:
        json.dump(data, file_pointer)


def get_filter_data(data):
    """
    Function: get_filter_data\n
    Parameters: data -> data to plot\n
    Functionality: Filter the data and return the filtered data\n
    """
    # print(data)
    dividend = 10
    filter_data = {}
    for key, frequency in data.items():
        new_key = key // dividend
        if new_key not in filter_data:
            filter_data[new_key] = [frequency]
        else:
            filter_data[new_key].append(frequency)
    new_data = {}
    for key, values in filter_data.items():
        new_data[key] = sum(values)
    data_x = [key for key, frequency in new_data.items()]
    summation = sum(data.values())
    data_y = [frequency / summation for key, frequency in new_data.items()]
    return (data_x, data_y)


def manage_all(degree_data, motif_data, degree_data_proposed, motif_data_proposed):
    """
    Function: manage_all\n
    Parameters: degree_data -> degree data for the GRN graph, motif_data -> motif data for the GRN graph, degree_data_proposed -> degree data for the Proposed graph, motif_data_proposed -> motif data for the Proposed graph\n
    Functionality: Manages the simulation\n
    """
    # Write data to file
    file_path = os.path.join(
        os.getcwd(), 'analysis_output_files', 'grn_properties_degree_plot.json')
    write_to_json(degree_data, file_path)
    file_path = os.path.join(
        os.getcwd(), 'analysis_output_files', 'grn_properties_motif_plot.json')
    write_to_json(motif_data, file_path)
    file_path = os.path.join(
        os.getcwd(), 'analysis_output_files', 'proposed_properties_degree_plot.json')
    write_to_json(degree_data_proposed, file_path)
    file_path = os.path.join(
        os.getcwd(), 'analysis_output_files', 'proposed_properties_motif_plot.json')
    write_to_json(motif_data_proposed, file_path)
    # End writing
    file_name = 'degree_distribution_grn_proposed.png'
    file_path = os.path.join(os.getcwd(), 'analysis_output_files', file_name)
    # Description of degree distribution plot
    data_x, data_y = get_filter_data(degree_data)
    data_x_proposed, data_y_proposed = get_filter_data(degree_data_proposed)
    plt.scatter(data_x, data_y, color='b')
    plt.scatter(data_x_proposed, data_y_proposed, color='r', marker='x')
    plt.ylabel('Frequency of occurance',
               fontsize=12, fontweight='bold')
    plt.xlabel('Degree of nodes', fontsize=12, fontweight='bold')
    # plt.title('Frequency Vs Degree of nodes',
    #           fontsize=17, fontweight='bold')
    plt.xticks(fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    plt.savefig(file_path)
    # Description of motif distribution plot
    file_name = 'motif_distribution_grn_proposed.png'
    file_path = os.path.join(os.getcwd(), 'analysis_output_files', file_name)
    data_x, data_y = get_filter_data(motif_data)
    data_x_proposed, data_y_proposed = get_filter_data(motif_data_proposed)
    plt.scatter(data_x, data_y, color='b')
    plt.scatter(data_x_proposed, data_y_proposed, color='r', marker='x')
    plt.ylabel('Frequency of occurance',
               fontsize=12, fontweight='bold')
    plt.xlabel('Node motif centrality of nodes',
               fontsize=12, fontweight='bold')
    # plt.title('Frequency Vs Node motif centrality of nodes',
    #           fontsize=17, fontweight='bold')
    plt.xticks(fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    plt.savefig(file_path)


def manage_TRN(degree_data, motif_data):
    """
    Function: manage_TRN\n
    Parameters: degree_data -> degree data for the GRN graph, motif_data -> motif data for the GRN graph\n
    Functionality: Manages the simulation\n
    """
    # Write data to file
    file_path = os.path.join(
        os.getcwd(), 'analysis_output_files', 'grn_properties_degree_plot.json')
    write_to_json(degree_data, file_path)
    file_path = os.path.join(
        os.getcwd(), 'analysis_output_files', 'grn_properties_motif_plot.json')
    write_to_json(motif_data, file_path)
    # End writing
    file_name = 'degree_distribution_grn_proposed.png'
    file_path = os.path.join(os.getcwd(), 'analysis_output_files', file_name)
    # Description of degree distribution plot
    data_x, data_y = get_filter_data(degree_data)
    # data_x_proposed, data_y_proposed = get_filter_data(degree_data_proposed)
    plt.bar(data_x, data_y, color='b')
    # plt.scatter(data_x_proposed, data_y_proposed, color='r', marker='x')
    plt.ylabel('Frequency of occurance',
               fontsize=12, fontweight='bold')
    plt.xlabel('Degree of nodes', fontsize=12, fontweight='bold')
    # plt.title('Frequency Vs Degree of nodes',
    #           fontsize=17, fontweight='bold')
    plt.xticks(fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    # plt.savefig(file_path)
    plt.show()
    # Description of motif distribution plot
    file_name = 'motif_distribution_grn_proposed.png'
    file_path = os.path.join(os.getcwd(), 'analysis_output_files', file_name)
    data_x, data_y = get_filter_data(motif_data)
    # data_x_proposed, data_y_proposed = get_filter_data(motif_data_proposed)
    plt.bar(data_x, data_y, color='b')
    # plt.scatter(data_x_proposed, data_y_proposed, color='r', marker='x')
    plt.ylabel('Frequency of occurance',
               fontsize=12, fontweight='bold')
    plt.xlabel('Node motif centrality of nodes',
               fontsize=12, fontweight='bold')
    # plt.title('Frequency Vs Node motif centrality of nodes',
    #           fontsize=17, fontweight='bold')
    plt.xticks(fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    # plt.savefig(file_path)
    plt.show()


def init_proposed():
    """
    Function: init_proposed\n
    Parameters: None\n
    Functionality: initialiazes the environment for the proposed algorithm\n
    """
    os.system('bash fresh_analysis.sh')
    os.system(f'{command} {script}')
    os.system(f'{command} main.py')
    global UAV_to_UAV_threshold, cell_size
    parent_dir = os.getcwd()
    target_dir = 'input_files'
    file_name = 'scenario_input.json'
    file_path = os.path.join(parent_dir, target_dir, file_name)
    with open(file_path, 'r') as file_pointer:
        data = json.load(file_pointer)
    UAV_to_UAV_threshold = data['UAV_to_UAV_threshold']
    cell_size = data['cell_size']
    parent_dir = os.getcwd()
    target_dir = 'graph_output_files'
    file_name = 'output_main0.json'
    file_path = os.path.join(parent_dir, target_dir, file_name)
    with open(file_path, 'r') as file_pointer:
        data = json.load(file_pointer)
    UAV_graph = get_UAV_graph(data)
    degrees_val = sorted([degree for node,
                          degree in UAV_graph.degree()])
    degrees_count = dict(collections.Counter(degrees_val))
    motifs_val = sorted([motif for node, motif in dict(
        grn_endpoint.grn_info.get_motif_dict(UAV_graph)).items()])
    motifs_count = dict(collections.Counter(motifs_val))
    return degrees_count, motifs_count


if __name__ == "__main__":
    dir_path = os.path.join(os.getcwd(), 'analysis_output_files')
    try:
        os.mkdir(dir_path)
    except OSError as error:
        pass
    degree_data, motif_data = init()
    # degree_data_proposed, motif_data_proposed = init_proposed()
    manage_TRN(degree_data, motif_data)

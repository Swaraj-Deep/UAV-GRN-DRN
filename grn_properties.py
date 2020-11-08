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


def get_filter_data(data, division_block):
    """
    Function: get_filter_data\n
    Parameters: data -> data to filter, division_block -> how the data will be divided\n
    Functionality: Filter the data and return the filtered data\n
    """
    filter_data = {}
    for key, value in data.items():
        if key // division_block in filter_data:
            filter_data[key // division_block].append(value)
        else:
            filter_data[key // division_block] = [value]
    new_data = {}
    for key, value in filter_data.items():
        value = pd.DataFrame(value).describe()[0]['50%']
        new_data[key] = value
    return new_data


def plot_option_one(data, file_path):
    """
    Function: plot_option_one\n
    Parameter: data -> data to plot, file_path -> path of the file to save the image\n
    Functionality: generate and save the bar plot\n
    """
    data_x = [degree for degree, frequency in data.items()]
    data_y = [frequency for degree, frequency in data.items()]
    plt.bar(data_x, data_y, color='r')
    plt.show()


def manage_all(degree_data, motif_data):
    """
    Function: manage_all\n
    Parameters: degree_data -> data for the degree graph, motif_data -> data for the motif graph\n
    Functionality: Manages the simulation\n
    """
    file_path = os.path.join(
        os.getcwd(), 'analysis_output_files', 'grn_properties_degree_plot.json')
    write_to_json(degree_data, file_path)
    file_path = os.path.join(
        os.getcwd(), 'analysis_output_files', 'grn_properties_motif_plot.json')
    write_to_json(motif_data, file_path)

    # Option one

    data = get_filter_data(degree_data, 10)
    plot_option_one(data, '')
    data = get_filter_data(motif_data, 5)
    plot_option_one(data, '')

    # Option Two

    # data_x = [degree for degree, frequency in degree_data.items()]
    # data_y = [frequency for degree, frequency in degree_data.items()]
    # plt.bar(data_x, data_y, color='r')
    # plt.xticks(np.arange(min(data_x), max(data_x)+1, 50.0))
    # plt.show()
    # data_x = [degree for degree, frequency in motif_data.items()]
    # data_y = [frequency for degree, frequency in motif_data.items()]
    # plt.bar(data_x, data_y, color='r')
    # plt.xticks(np.arange(min(data_x), max(data_x)+1, 50.0))
    # plt.show()

    # Option Three

    # data_x = [degree for degree, frequency in degree_data.items()]
    # data_y = [frequency for degree, frequency in degree_data.items()]
    # plt.bar(data_x, data_y, color='r')
    # plt.xscale("log")
    # plt.show()
    # data_x = [degree for degree, frequency in motif_data.items()]
    # data_y = [frequency for degree, frequency in motif_data.items()]
    # plt.bar(data_x, data_y, color='r')
    # plt.xscale("log")
    # plt.show()


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
    # degree_data, motif_data = init()
    degree_data, motif_data = init_proposed()
    print(degree_data)
    manage_all(degree_data, motif_data)

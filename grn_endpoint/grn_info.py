import networkx as nx
import pickle
import os
import random

# Variable to hold the GRN graph

grn_graph = 0


def get_grn_graph():
    """
    Function: get_grn_graph\n
    Parameters: None\n
    Returns: The grn_graph which we are working on\n
    """
    return grn_graph


def get_motif_dict(grn_graph):
    """
    Function: get_motif_dict
    Parameter: grn_graph -> Corresponding GRN graph
    Returns: node motif centrality of the GRN graph
    """
    node_motif_centrality_dict = {}
    for node in grn_graph.nodes:
        node_motif_centrality_dict[node] = 0
    if grn_graph.is_directed():
        for u in grn_graph.nodes:
            for v in grn_graph.nodes:
                for w in grn_graph.nodes:
                    if grn_graph.has_edge(u, v) and grn_graph.has_edge(v, w) and grn_graph.has_edge(u, w):
                        node_motif_centrality_dict[u] += 1
                        node_motif_centrality_dict[v] += 1
                        node_motif_centrality_dict[w] += 1
    else:
        for u in grn_graph.nodes:
            for v in grn_graph.nodes:
                if v <= u:
                    continue
                for w in grn_graph.nodes:
                    if w <= v:
                        continue
                    if grn_graph.has_edge(u, v) and grn_graph.has_edge(v, w) and grn_graph.has_edge(u, w):
                        node_motif_centrality_dict[u] += 1
                        node_motif_centrality_dict[v] += 1
                        node_motif_centrality_dict[w] += 1
    return node_motif_centrality_dict


# Global Variable to find the highest edge motif centrality of the GRN

PI = 0

# Dictionary of GRN_edges i.e which of the edges are present in the GRN graph
# The key in this dictionary is a tuple representing an edge
# The value is True of all the keys as it contains only that edge which is present in the GRN graph

GRN_edges = {}

# Dictionary of the edge motif centrality of the GRN graph
# The key in this dictionary is the edge in the GRN graph
# The value is the edge motif centrality of that edge

e_motif = {}

# Dictionary containing the node motif centrality of the GRN graph
# The key in this dictionary is the node in the GRN graph
# The value is the node motif centrality of that node

n_motif = {}

# Dictionary of mapping of the UAVs to the sorted order of the GRN nodes (according to the node motif centrality in reverse order)
# The key in this dictionary is the UAV node
# The value is the mapped gene in the GRN graph

mapping = {}


def get_n_motif():
    """
    Function: get_n_motif\n
    Parameter: None\n
    returns: Node motif centrality of the grn graph
    """
    global n_motif
    return n_motif

def get_emc(u, v):
    """
    Function: get_emc\n
    Parameters: u -> start node of the edge, v -> end node of the edge\n
    Returns: edge motif centrality of the passed edge if that edge exists else return 0\n
    """
    edge = (u, v)
    if edge in e_motif:
        return e_motif[edge]
    return 0


def get_nmc(node):
    """
    Function: get_nmc\n
    Parameter: node -> node of the grn\n
    Returns: node motif centrality of the passed node if that node exists else return 0\n
    """
    if node in n_motif:
        return n_motif[node]
    return 0


def m(UAV_node):
    """
    Function: m\n
    Parameter: UAV_node -> node in the UAV set\n
    Returns: the gene which is mapped to that UAV_node if there exists a mapping else return 0\n
    """
    if UAV_node in mapping:
        return mapping[UAV_node]
    return 0


def is_edge_grn(u, v):
    """
    Function: is_edge_grn\n
    Parameter: u -> start node of the edge, v -> end node of the edge\n
    Returns: returns True if the edge (u, v) exists in the GRN graph else False\n
    """
    edge = (u, v)
    if edge in GRN_edges:
        return True
    return False


def get_PI():
    """
    Function: get_PI\n
    Parameter: None\n
    Returns: returns the value of PI
    """
    return PI


def generate_subgraph(grn_graph, number_nodes, output_file_name):
    """
    Function: generate_subgraph\n
    Parameter: grn_graph -> the source graph, number_nodes -> number of nodes to subgraph, output_file_name -> Name of the output file
    Return: nothing
    Functionality: Saves the file in the root directory
    """
    SG = grn_graph.__class__()
    node = [i for i in range(number_nodes)]
    SG = grn_graph.subgraph(node)
    nx.write_gml(SG, output_file_name)


def subgraph_on_motif_centrality(non_increasing_grn_nodes, grn_graph, number_genes, req_per, file_name):
    """
    Function: subgraph_on_motif_centrality\n
    Parameter: non_increasing_grn_nodes -> list of genes arranged in non increasing order of their node motif centrality, grn_graph -> The GRN graph, number_genes -> number of genes to generate subgraph from, req_per -> Percentatge of extra random edges , file_name -> file name of the output subgraph\n
    Functionality: generates subgraph based on the node motif centrality\n
    """
    mapped_genes = set()
    mapped_genes.add(non_increasing_grn_nodes[0])
    non_increasing_grn_nodes.remove(non_increasing_grn_nodes[0])
    while (len(mapped_genes) < number_genes):
        flag = False
        for gene in non_increasing_grn_nodes:
            for mapped_gene in mapped_genes:
                if (gene, mapped_gene) in grn_graph.edges:
                    mapped_genes.add(gene)
                    non_increasing_grn_nodes.remove(gene)
                    flag = True
                    break
                elif (mapped_gene, gene) in grn_graph.edges:
                    mapped_genes.add(gene)
                    non_increasing_grn_nodes.remove(gene)
                    flag = True
                    break
            if flag:
                break
    node_list = list(mapped_genes)
    edge_list = []
    for node1 in node_list:
        for node2 in node_list:
            if node1 != node2:
                if (node1, node2) in grn_graph.edges:
                    edge_list.append((node1, node2))
                elif (node2, node1) in grn_graph.edges:
                    edge_list.append((node2, node1))
    SG = grn_graph.__class__()
    SG.add_nodes_from(node_list)
    for edge in edge_list:
        u, v = edge
        SG.add_edge(u, v)
    old_edges = len (SG.edges)
    new_edges = int(old_edges * req_per)
    nodes = list(SG.nodes)
    new_edge_list = []
    while len(new_edge_list) < new_edges:
        a = random.randint(0, len(nodes) - 1)
        b = random.randint(0, len(nodes) - 1)
        u = nodes[a]
        v = nodes[b]
        if (u, v) not in edge_list:
            new_edge_list.append((u, v))
    for edge in new_edge_list:
        u, v = edge
        SG.add_edge(u, v)
    nx.write_gml(SG, file_name)


def write_binary(n_motif_centrality_dict, file_name):
    """
    Function: write_binary\n
    Parameter: n_motif_centrality_dict -> dictionary of node motifs, file_name -> file name of the binary output\n
    Returns: nothing\n
    Functionality: Writes node motif centrality dict to the passed file_name\n
    """
    pickle.dump(n_motif_centrality_dict, open(file_name, "wb"))


def init():
    """
    Function: init
    Parameter: none
    Functionality: Initializes the variables
    """
    global grn_graph
    parent_path = os.getcwd()
    file_prefix = '400'
    file_name = file_prefix + '.gml'
    grn_file_path = os.path.join(parent_path, 'grn_endpoint', file_name)
    grn_graph = nx.read_gml(grn_file_path)
    grn_graph = nx.convert_node_labels_to_integers(grn_graph, first_label=0)
    global n_motif
    global e_motif
    global mapping
    global PI
    centrality_file = file_prefix + '_centrality.p'
    centrality_file_path = os.path.join(
        parent_path, 'grn_endpoint', centrality_file)
    n_motif = pickle.load(open(centrality_file_path, "rb"))
    for edge in grn_graph.edges:
        node1, node2 = edge
        e_motif[edge] = min(n_motif[node1], n_motif[node2])
        PI = max(PI, e_motif[edge])
    non_increasing_grn_nodes = [node[0]
                                for node in sorted(n_motif.items(), key=lambda node: node[1], reverse=True)]
    mapping_function(non_increasing_grn_nodes, grn_graph)
    for edge in grn_graph.edges:
        GRN_edges[edge] = True


def old_mapping_function(non_increasing_grn_nodes):
    """
    Function: old_mapping_function\n
    Parameter: non_increasing_grn_nodes -> list of genes arranged in non increasing order of their node motif centrality\n
    Functionality: Fills the dictionary mapping\n
    """
    global mapping
    for node, grn_node in enumerate(non_increasing_grn_nodes):
        mapping[node + 1] = grn_node


def mapping_function(non_increasing_grn_nodes, grn_graph):
    """
    Function: mapping_function\n
    Parameter: non_increasing_grn_nodes -> list of genes arranged in non increasing order of their node motif centrality, grn_graph -> The GRN graph\n
    Functionality: Fills the dictionary mapping\n
    """
    global mapping
    mapping = {}
    mapped_genes = set()
    mapped_genes.add(non_increasing_grn_nodes[0])
    mapping[1] = non_increasing_grn_nodes[0]
    UAVs = len(non_increasing_grn_nodes)
    non_increasing_grn_nodes.remove(non_increasing_grn_nodes[0])
    UAV_node = 2
    while (UAV_node <= UAVs):
        flag = False
        for gene in non_increasing_grn_nodes:
            for mapped_gene in mapped_genes:
                if (gene, mapped_gene) in grn_graph.edges:
                    mapping[UAV_node] = gene
                    mapped_genes.add(gene)
                    non_increasing_grn_nodes.remove(gene)
                    flag = True
                    break
                elif (mapped_gene, gene) in grn_graph.edges:
                    mapping[UAV_node] = gene
                    mapped_genes.add(gene)
                    non_increasing_grn_nodes.remove(gene)
                    flag = True
                    break
            if flag:
                break
        UAV_node += 1


if __name__ == "__main__":
    init()

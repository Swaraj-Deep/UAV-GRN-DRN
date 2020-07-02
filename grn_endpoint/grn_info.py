import networkx as nx
import pickle
import os


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


def init():
    """
    Function: init
    Parameter: none
    Functionality: Initializes the variables
    """
    parent_path = os.getcwd()
    file_name = 'grn_endpoint/100.gml'
    file_path = os.path.join(parent_path, file_name)
    grn_graph = nx.read_gml(file_path)
    grn_graph = nx.convert_node_labels_to_integers(grn_graph, first_label=0)
    global n_motif
    global e_motif
    global mapping
    global PI
    n_motif = get_motif_dict(grn_graph)
    for node1 in grn_graph.nodes:
        for node2 in grn_graph.nodes:
            if [node1, node2] in grn_graph.edges:
                e_motif[(node1, node2)] = min(n_motif[node1], n_motif[node2])
                PI = max(PI, e_motif[(node1, node2)])
    non_increasing_grn_nodes = [node[0]
                                for node in sorted(n_motif.items(), key=lambda node: node[1], reverse=True)]
    for node, grn_node in enumerate(non_increasing_grn_nodes):
        mapping[node] = grn_node
    for edge in grn_graph.edges:
        GRN_edges[edge] = True


def init_3000():
    """
    Function: init_3000\n
    Parameters: None\n
    Functionality: Initialiazes the global variables\n
    """
    parent_dir = os.getcwd()
    file_path = os.path.join(parent_dir, 'grn_endpoint', '4441_centrality.p')
    global n_motif
    global e_motif
    global mapping
    global PI
    n_motif = pickle.load(open(file_path, "rb"))
    parent_path = os.getcwd()
    file_path = os.path.join(parent_path, 'grn_endpoint', '4441.gml')
    grn_graph = nx.read_gml(file_path)
    grn_graph = nx.convert_node_labels_to_integers(grn_graph, first_label=0)
    for edge in grn_graph.edges:
        node1, node2 = edge
        e_motif[edge] = min(n_motif[node1], n_motif[node2])
        PI = max(PI, e_motif[edge])
    non_increasing_grn_nodes = [node[0]
                                for node in sorted(n_motif.items(), key=lambda node: node[1], reverse=True)]
    for node, grn_node in enumerate(non_increasing_grn_nodes):
        mapping[node] = grn_node
    for edge in grn_graph.edges:
        GRN_edges[edge] = True


if __name__ == "__main__":
    init_3000()

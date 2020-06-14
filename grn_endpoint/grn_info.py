# Dictionary of GRN_edges i.e which of the edges are present in the GRN graph
# The key in this dictionary is a tuple representing an edge
# The value is True of all the keys as it contains only that edge which is present in the GRN graph

GRN_edges = {
    ('a', 'b'): True,
    ('b', 'c'): True,
    ('b', 'g'): True,
    ('b', 'd'): True,
    ('c', 'd'): True,
    ('g', 'd'): True,
    ('d', 'e'): True,
    ('d', 'f'): True,
    ('e', 'f'): True
}

# Dictionary of the edge motif centrality of the GRN graph
# The key in this dictionary is the edge in the GRN graph
# The value is the edge motif centrality of that edge

e_motif = {
    ('a', 'b'): 0,
    ('b', 'c'): 1,
    ('b', 'g'): 1,
    ('b', 'd'): 2,
    ('c', 'd'): 1,
    ('g', 'd'): 1,
    ('d', 'e'): 1,
    ('d', 'f'): 1,
    ('e', 'f'): 1
}

# Dictionary containing the node motif centrality of the GRN graph
# The key in this dictionary is the node in the GRN graph
# The value is the node motif centrality of that node

n_motif = {
    'd': 3,
    'b': 2,
    'c': 1,
    'g': 1,
    'e': 1,
    'f': 1,
    'a': 0
}

# Dictionary of mapping of the UAVs to the sorted order of the GRN nodes (according to the node motif centrality in reverse order)
# The key in this dictionary is the UAV node
# The value is the mapped gene in the GRN graph

mapping = {
    1: 'd',
    2: 'b',
    3: 'c',
    4: 'g',
    5: 'e',
    6: 'f',
    7: 'a'
}


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
    Function: is_edge_grn
    Parameter: u -> start node of the edge, v -> end node of the edge\n
    Returns: returns True if the edge (u, v) exists in the GRN graph else False\n
    """
    edge = (u, v)
    if edge in GRN_edges:
        return True
    return False

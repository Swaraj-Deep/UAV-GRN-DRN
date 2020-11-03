import os
import json
import grn_endpoint.grn_info
import collections
import matplotlib.pyplot as plt


def init():
    """
    Function: init\n
    Parameter: None\n
    Functionality: Initialiazes the GRN environment\n
    """
    grn_endpoint.grn_info.init()


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


if __name__ == "__main__":
    init()
    print('Degree Count', get_degree_count())
    print('Motif Count', get_motif_count())
    data = get_degree_count()
    data_x = [degree for degree, frequency in data.items()]
    data_y = [frequency for degree, frequency in data.items()]
    plt.bar(data_x, data_y, color='r')
    plt.show()

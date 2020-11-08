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
    data = {1: 19, 2: 8, 3: 77, 4: 90, 5: 52, 6: 75, 7: 22, 8: 17, 9: 6, 10: 2, 11: 3, 12: 2, 13: 4, 14: 1, 15: 3, 17: 2, 21: 1, 23: 3, 24: 1, 28: 1, 30: 1, 36: 2, 50: 1, 54: 1, 72: 1}
    data_x = [degree for degree, frequency in data.items()]
    print(data_x)
    data_y = [frequency for degree, frequency in data.items()]
    print(max(data_x))
    # print(max(data_y))
    plt.bar(data_x, data_y, color='r')
    # plt.xscale("log")
    plt.xticks(data_x)
    plt.show()

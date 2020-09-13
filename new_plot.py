import json
import os
import random
import networkx as nx

def input_graph(file_type):
    """
    Function: input_graph\n
    Parameters: None\n
    Functionality: Input the graph which is the output of Either of the algorithms i.e. main.py or baseline.py
    """
    parent_dir = os.getcwd()
    dir_name = 'graph_output_files'
    for file in os.listdir(os.path.join(parent_dir, dir_name)):
        if file_type in file:
            print(file)
            
input_graph('baseline')

import os
import os.path
import sys


def update_main_file(type):
    """
    Function: update_main_file\n
    Parameters: type -> whether bruteforce or q_learn\n
    Functionality: Update Main file according to bruteforce or q_learn
    """
    parent_dir = os.getcwd()
    file_name = 'main.py'
    file_path = os.path.join(parent_dir, file_name)
    file_data = []
    with open(file_path, 'r') as file_pointer:
        file_data = file_pointer.readlines()
        line_to_change1 = file_data[307].split('=')
        line_to_change2 = file_data[342].split('=')
        line_to_change3 = file_data[385].split('=')
        if type == 'bruteforce':
            line_to_change1[1] = 'bruteforce(UAV_node, placed, True)\n'
            line_to_change2[1] = 'bruteforce(UAV_node, placed, False)\n'
            line_to_change3[1] = 'bruteforce(UAV_node, placed, False)\n'
        else:
            line_to_change1[1] = 'q_learn(UAV_node, placed, True)\n'
            line_to_change2[1] = 'q_learn(UAV_node, placed, False)\n'
            line_to_change3[1] = 'q_learn(UAV_node, placed, False)\n'
    file_data[307] = '= '.join(line_to_change1)
    file_data[342] = '= '.join(line_to_change2)
    file_data[385] = '= '.join(line_to_change3)
    with (open(file_path, 'w')) as file_pointer:
        file_pointer.writelines(file_data)


def call_update():
    """
    Function: call_update\n
    Parameters: None\n
    Functionality: To call the update function
    """
    update_main_file(sys.argv[1])


call_update()

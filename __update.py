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
        line_to_change = file_data[263].split('=')
        if type == 'bruteforce':
            line_to_change[1] = 'bruteforce(UAV_node, placed)\n'
        else:
            line_to_change[1] = 'q_learn(UAV_node, placed)\n'
    file_data[263] = '= '.join(line_to_change)
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

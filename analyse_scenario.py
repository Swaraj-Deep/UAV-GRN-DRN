import os
import os.path
import json
import time

# List to hold different scenario size

size = [10, 15, 20, 25, 30]

# List to hold number of users in each scenario

users = [20, 60, 80, 100, 180]

# Maximum range of UAV to UAV communication threshold

UAV_to_UAV_threshold = 30


def find_percentage(lines, num_ahead):
    """
    Function: find_percentage\n
    Parameter: lines -> lines of current output file opened, num_ahead -> number of lines ahead where we get the percentage of edge similarity\n
    Returns: edge similarity percentage in that file
    """
    percentage = 0.0
    if 'Following' in lines[3 + num_ahead]:
        if 'Following' in lines[3 + num_ahead + 2]:
            percentage = lines[3 + num_ahead + 5].split(':')[1]
        elif 'graph' in lines[3 + num_ahead + 2]:
            percentage = lines[3 + num_ahead + 4].split(':')[1]
    elif 'graph' in lines[3 + num_ahead]:
        if 'Following' in lines[3 + num_ahead + 1]:
            percentage = lines[3 + num_ahead + 4].split(':')[1]
        elif 'graph' in lines[3 + num_ahead + 1]:
            percentage = lines[3 + num_ahead + 3].split(':')[1]
    return percentage


def check_if_complete():
    """
    Function: check_if_complete\n
    Parameter: None\n
    Returns: True if criteria is met\n
    """
    epsilon = 0.0
    learning_rate = 0.0
    decay_factor = 0.0
    with open('input_files/scenario_input.json', 'r') as file_pointer:
        file_data = json.load(file_pointer)
        epsilon = file_data['epsilon']
        learning_rate = file_data['learning_rate']
        decay_factor = file_data['decay_factor']
    parent_dir = './output_files'
    curr_dir = str(epsilon) + "_" + str(learning_rate) + \
        "_" + str(decay_factor)
    dir_path = os.path.join(parent_dir, curr_dir)
    file_name = 'Output_text0.txt'
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r') as file_pointer:
        lines = file_pointer.readlines()
    curr_user_served = int(lines[0].split(':')[1])
    curr_UAV_used = int(lines[2].split(':')[1])
    similarity_percentage = float(
        find_percentage(lines, curr_UAV_used))
    print(similarity_percentage)


def update_scenario_input():
    """
    Function: update_scenario_input\n
    Parameters: None\n
    Functionality: Update the scenario_input.json file\n
    """
    parent_dir = os.getcwd()
    folder_name = 'input_files'
    for thresold in range(6, UAV_to_UAV_threshold + 1):
        file_name = 'scenario_input.json'
        file_path = os.path.join(parent_dir, folder_name, file_name)
        with open(file_path, 'r') as file_pointer:
            scenario_data = json.load(file_pointer)
        scenario_data['UAV_to_UAV_threshold'] = thresold
        with open(file_path, 'w') as file_pointer:
            json.dump(scenario_data, file_pointer)
        os.system('python3 main.py')
        check_if_complete()
        os.system('./fresh_analysis.sh')


def runner_function():
    """
    Function: runner_function\n
    Parameters: None\n
    Functionality: Automates the analysis\n
    """
    parent_dir = os.getcwd()
    folder_name = 'input_files'
    file_name = 'user_location.json'
    file_path = os.path.join(parent_dir, folder_name, file_name)
    for i in range(len(size)):
        with open(file_path, 'r') as file_pointer:
            file_data = json.load(file_pointer)
        file_data['N'] = size[i]
        file_data['Number of User'] = users[i]
        with open(file_path, 'w') as file_pointer:
            json.dump(file_data, file_pointer)
        os.system('python3 user_secnario_producer.py')
        update_scenario_input()


runner_function()

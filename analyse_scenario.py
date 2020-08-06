import os
import os.path
import json

# List to hold different scenario size

size = [10, 15, 20, 25, 30]

# List to hold number of users in each scenario

users = [20, 60, 80, 100, 180]

# Maximum range of UAV to UAV communication threshold

UAV_to_UAV_threshold = 30


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
        with open (file_path, 'w') as file_pointer:
            json.dump (file_data, file_pointer)
        os.system('python3 user_secnario_producer.py')

runer()


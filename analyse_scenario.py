import os
import os.path
import json
import time

# List to hold different scenario size

size = [15]

# List to hold number of users in each scenario

users = [60]

# Range of UAV to UAV communication

min_communication_threshold = 6
max_communication_threshold = 40
UAV_to_UAV_threshold = [str(i)+'.'+str(j)+''+str(k) for i in range(min_communication_threshold,
                                                                   max_communication_threshold) for j in range(0, 10) for k in range(0, 10)]

# Maximum number of iteration

max_iter = 10


def update_log_file(threshold, sd_user_dist):
    """
    Function: update_log_file\n
    Parameters: therhold -> threshold of the UAV to UAV communication, sd_user_dist -> standard deviation of user distances\n
    Functionality: Appends new data to the log file\n
    """
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    final_log_file = 'scenario_analysis.log'
    lines_to_write = []
    lines_to_write.append(
        f'{threshold} {sd_user_dist}\n')
    with open(os.path.join(parent_dir, dir_name, final_log_file), 'a') as file_pointer:
        file_pointer.writelines(lines_to_write)


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


def list_file_data():
    """
    Function: list_file_data\n
    Parameters: None\n
    Return: list of data in output file\n
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
    return lines


def check_if_complete():
    """
    Function: check_if_complete\n
    Parameter: None\n
    Returns: True if criteria is met\n
    """
    lines = list_file_data()
    curr_user_served = int(lines[0].split(':')[1])
    curr_UAV_used = int(lines[2].split(':')[1])
    similarity_percentage = float(
        find_percentage(lines, curr_UAV_used))
    sd_user_dist = float(lines[-2].split(':')[1])
    parent_dir = os.getcwd()
    folder_name = 'input_files'
    file_name = 'scenario_input.json'
    file_path = os.path.join(parent_dir, folder_name, file_name)
    with open(file_path, 'r') as file_pointer:
        scenario_data = json.load(file_pointer)
    expected_similarity = scenario_data['similarity_threshold'] * 100
    if similarity_percentage >= expected_similarity:
        N = scenario_data['N']
        threshold = scenario_data['UAV_to_UAV_threshold']
        return True
    return False


def update_scenario_input():
    """
    Function: update_scenario_input\n
    Parameters: None\n
    Functionality: Update the scenario_input.json file\n
    """
    global UAV_to_UAV_threshold
    parent_dir = os.getcwd()
    folder_name = 'input_files'
    low = 0
    high = len(UAV_to_UAV_threshold) - 1
    minm_threshold = 999999999
    sd_user_dist = 0
    while low <= high:
        mid = (low + high) // 2
        threshold = float(UAV_to_UAV_threshold[mid])
        file_name = 'scenario_input.json'
        file_path = os.path.join(parent_dir, folder_name, file_name)
        with open(file_path, 'r') as file_pointer:
            scenario_data = json.load(file_pointer)
        scenario_data['UAV_to_UAV_threshold'] = threshold
        with open(file_path, 'w') as file_pointer:
            json.dump(scenario_data, file_pointer)
        os.system('python3 main.py')
        if check_if_complete():
            high = mid - 1
            if threshold < minm_threshold:
                minm_threshold = threshold
                lines = list_file_data()
                sd_user_dist = float(lines[-2].split(':')[1])
            os.system('bash fresh_analysis.sh')
        else:
            low = mid + 1
            os.system('bash fresh_analysis.sh')
    update_log_file(minm_threshold, sd_user_dist)


def runner_function():
    """
    Function: runner_function\n
    Parameters: None\n
    Functionality: Automates the analysis\n
    """
    global size
    global users
    parent_dir = os.getcwd()
    os.system('bash fresh_analysis.sh')
    final_log_file = 'scenario_analysis.log'
    lines_to_write = []
    lines_to_write.append(
        f'###############################################################################################\n')
    lines_to_write.append(
        f'################################## Final Analysis Report ######################################\n')
    lines_to_write.append(
        f'###############################################################################################\n')
    with open(os.path.join(parent_dir, 'analysis_output_files', final_log_file), 'w') as file_pointer:
        file_pointer.writelines(lines_to_write)
    folder_name = 'input_files'
    file_name = 'user_location.json'
    file_path = os.path.join(parent_dir, folder_name, file_name)
    for i in range(len(size)):
        with open(file_path, 'r') as file_pointer:
            file_data = json.load(file_pointer)
        file_data['N'] = size[i]
        file_data['M'] = size[i]
        file_data['Number of User'] = users[i]
        with open(file_path, 'w') as file_pointer:
            json.dump(file_data, file_pointer)
        for iter in range(max_iter):
            os.system('python3 user_secnario_producer.py')
            update_scenario_input()
    lines_to_write = []
    lines_to_write.append(
        f'###############################################################################################\n')
    lines_to_write.append(
        f'###################################### END OF REPORT ##########################################\n')
    lines_to_write.append(
        f'###############################################################################################\n')
    with open(os.path.join(parent_dir, 'analysis_output_files', final_log_file), 'a') as file_pointer:
        file_pointer.writelines(lines_to_write)


if __name__ == "__main__":
    dir_path = os.path.join(os.getcwd(), 'analysis_output_files')
    try:
        os.mkdir(dir_path)
    except OSError as error:
        pass
    print("Relax!! We have taken the charge:)")
    runner_function()
    os.system("python3 plot_graph.py")

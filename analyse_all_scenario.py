import os
import os.path
import json
import time

# List to hold different scenario size

size = [5, 10, 15, 20]

# List to hold number of users in each scenario

users = [5, 20, 45, 80]

# Range of UAV to UAV communication

min_communication_threshold = 1
max_communication_threshold = 40
UAV_to_UAV_threshold = [str(i)+'.'+str(j)+''+str(k) for i in range(min_communication_threshold,
                                                                   max_communication_threshold) for j in range(0, 10) for k in range(0, 10)]

# Maximum number of iteration

max_iter = 1


def update_log_file(threshold, sd_user_dist, curr_user_served, curr_UAV_used, similarity_percentage, N):
    """
    Function: update_log_file\n
    Parameters: therhold -> threshold of the UAV to UAV communication, sd_user_dist -> standard deviation of user distances, curr_user_served -> user served with current UAVs, curr_UAV_used -> Number of UAVs used to serve users, similarity_percentage -> Similarity percentage of UAV graph, N -> Grid Size\n
    Functionality: Appends new data to the log file\n
    """
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    final_log_file = 'scenario_analysis.log'
    lines_to_write = []
    lines_to_write.append(
        f'# Area Size: {N} X {N}\n# UAV used: {curr_UAV_used}\n# User covered: {curr_user_served}\n# Edge Similarity Percentage: {similarity_percentage}\n# Standard Deviation of user location: {sd_user_dist}\n# UAV Communication Threshold: {threshold}\n')
    with open(os.path.join(parent_dir, dir_name, final_log_file), 'a') as file_pointer:
        file_pointer.writelines(lines_to_write)


def list_file_data():
    """
    Function: list_file_data\n
    Parameters: None\n
    Return: list of data in analysis.log file\n
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
    file_name = 'analysis.log'
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
    curr_user_served = round(float(lines[27].split(':')[1]), 2)
    curr_UAV_used = round(float(lines[13].split(':')[1]), 2)
    similarity_percentage = round(float(lines[20].split(':')[1]), 2)
    sd_user_dist = round(float(lines[28].split(':')[1]), 2)
    parent_dir = os.getcwd()
    folder_name = 'input_files'
    file_name = 'scenario_input.json'
    file_path = os.path.join(parent_dir, folder_name, file_name)
    with open(file_path, 'r') as file_pointer:
        scenario_data = json.load(file_pointer)
    expected_similarity = scenario_data['similarity_threshold'] * 100
    N = scenario_data['N']
    if similarity_percentage >= expected_similarity:
        threshold = scenario_data['UAV_to_UAV_threshold']
        return (True, curr_user_served, curr_UAV_used, similarity_percentage, sd_user_dist, N)
    return (False, curr_user_served, curr_UAV_used, similarity_percentage, sd_user_dist, N)


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
    min_threshold = 999999999
    min_sd_user_dist = 0
    min_curr_user_served = 0
    min_curr_UAV_used = 0
    min_similarity_percentage = 0
    min_N = 0
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
        for iter in range(max_iter):
            os.system('python3 user_secnario_producer.py')
            os.system('python3 main.py')
        os.system('python3 analysis.py')
        is_done, curr_user_served, curr_UAV_used, similarity_percentage, sd_user_dist, N = check_if_complete()
        if is_done:
            high = mid - 1
            if threshold < min_threshold:
                min_threshold = threshold
                min_sd_user_dist = sd_user_dist
                min_curr_user_served = curr_user_served
                min_curr_UAV_used = curr_UAV_used
                min_similarity_percentage = similarity_percentage
                min_N = N
            os.system('bash fresh_analysis.sh')
        else:
            low = mid + 1
            os.system('bash fresh_analysis.sh')
    update_log_file(min_threshold, min_sd_user_dist, min_curr_user_served,
                    min_curr_UAV_used, min_similarity_percentage, min_N)


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
        file_data['Number of User'] = users[i]
        with open(file_path, 'w') as file_pointer:
            json.dump(file_data, file_pointer)
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
    print("Relax!! We have taken the charge:)")
    runner_function()
    os.system("python3 plot_graph.py")

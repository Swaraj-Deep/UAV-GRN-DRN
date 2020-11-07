import os
import json
import matplotlib.pyplot as plt

number_UAVs = [1, 2, 4, 8, 16, 32]
command = "python3"
script = "user_secnario_producer.py"


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


def execute():
    """
    Function: execute\n
    Parameter: None\n
    Functionality: Execute the  main file\n
    """
    global command
    os.system('./fresh_analysis.sh')
    os.system(f'{command} main.py')


def get_output_directory():
    """
    Function: get_output_directory\n
    Parameter: None\n
    Returns: Path of the output directory\n
    """
    epsilon = 0.0
    learning_rate = 0.0
    decay_factor = 0.0
    parent_dir = os.getcwd()
    input_folder = 'input_files'
    file_name = 'scenario_input.json'
    with open(os.path.join(parent_dir, input_folder, file_name), 'r') as file_pointer:
        file_data = json.load(file_pointer)
        epsilon = file_data['epsilon']
        learning_rate = file_data['learning_rate']
        decay_factor = file_data['decay_factor']
    output_dir = 'output_files'
    curr_dir = str(epsilon) + "_" + str(learning_rate) + \
        "_" + str(decay_factor)
    return os.path.join(parent_dir, output_dir, curr_dir)


def get_grounduser_and_similarity():
    """
    Function: get_grounduser_and_similarity\n
    Parameter: None\n
    Returns: Tuple of groundUser covered and similarity percentage\n
    """
    dir_path = get_output_directory()
    with open(os.path.join(dir_path, 'Output_text1.txt'), 'r') as file_pointer:
        lines = file_pointer.readlines()
    curr_user_served = int(lines[0].split(':')[1])
    curr_UAV_used = int(lines[2].split(':')[1])
    similarity_percentage = float(
        find_percentage(lines, curr_UAV_used))
    return (curr_user_served, similarity_percentage)


def line_plot(graph_data):
    """
    Function: plot\n
    Parameter: graph_data -> dictionary where key is the number of UAVs given and value is the tuple of ground user covered and similarity percentage\n
    Functionality: Draws a line plot\n
    """
    x_val = [key for key in graph_data]
    ground_user_covered = [value[0] for key, value in graph_data.items()]
    similarity_percentage = [value[1] for key, value in graph_data.items()]
    plt.scatter(x_val, ground_user_covered)
    plt.plot(x_val, ground_user_covered, label="Ground User served")
    plt.scatter(x_val, similarity_percentage)
    plt.plot(x_val, similarity_percentage, label="Similarity Percentage")
    plt.ylabel('Ground User covered and Similarity percentage',
               fontsize=12, fontweight='bold')
    plt.xlabel('Maximum Number of UAVs', fontsize=12, fontweight='bold')
    plt.title('Variation of user coverage and similarity percentage',
              fontsize=12, fontweight='bold')
    plt.xticks(fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    plt.legend()
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'GUandSimilarity.png'
    file_path = os.path.join(parent_dir, dir_name, file_name)
    plt.savefig(file_path)


def init():
    """
    Function: init\n
    Parameter: None\n
    Functionality: Initializes the environment\n
    """
    global number_UAVs
    graph_data = {}
    os.system('./fresh_analysis.sh')
    parent_dir = os.getcwd()
    target_dir = 'input_files'
    file_name = 'scenario_input.json'
    file_path = os.path.join(parent_dir, target_dir, file_name)
    global script, command
    os.system(f'{command} {script}')
    for number_UAV in number_UAVs:
        with open(file_path, 'r') as file_pointer:
            data = json.load(file_pointer)
        data['number_UAV'] = number_UAV
        with open(file_path, 'w') as file_pointer:
            json.dump(data, file_pointer)
        execute()
        graph_data[number_UAV] = get_grounduser_and_similarity()
    line_plot(graph_data)


if __name__ == "__main__":
    init()

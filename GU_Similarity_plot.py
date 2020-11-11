import os
import json
import matplotlib.pyplot as plt

number_UAVs = [4, 8, 16, 32]
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
    os.system('bash fresh_analysis.sh')
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


def get_grounduser_and_similarity(number_users):
    """
    Function: get_grounduser_and_similarity\n
    Parameter: number_users -> number of users in the environment\n
    Returns: Tuple of groundUser covered and similarity percentage\n
    """
    dir_path = get_output_directory()
    with open(os.path.join(dir_path, 'Output_text1.txt'), 'r') as file_pointer:
        lines = file_pointer.readlines()
    curr_user_served = int(lines[0].split(':')[1])
    curr_UAV_used = int(lines[2].split(':')[1])
    similarity_percentage = float(
        find_percentage(lines, curr_UAV_used))
    return (curr_user_served / number_users, similarity_percentage)


def line_plot(graph_data):
    """
    Function: plot\n
    Parameter: graph_data -> dictionary where key is the number of UAVs given and value is the tuple of ground user covered and similarity percentage\n
    Functionality: Draws a line plot\n
    """
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'GUNewPlot.png'
    file_path = os.path.join(parent_dir, dir_name, file_name)
    x_val = [key for key in graph_data]
    ground_user_covered = [value[0] for key, value in graph_data.items()]
    similarity_percentage = [value[1] for key, value in graph_data.items()]
    # Ground User percentage
    plt.scatter(x_val, ground_user_covered)
    plt.plot(x_val, ground_user_covered, label="Ground User served")
    plt.ylabel('Percentage of Ground User covered',
               fontsize=12, fontweight='bold')
    plt.xlabel('Number of UAVs', fontsize=12, fontweight='bold')
    plt.title('User coverage percentage Vs Number of UAVs',
              fontsize=12, fontweight='bold')
    plt.xticks(fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    plt.legend()
    # plt.savefig(file_path)
    plt.show()
    # Clear plot
    plt.clf()
    # Similarity Percentage
    plt.scatter(x_val, similarity_percentage)
    plt.plot(x_val, similarity_percentage, label="Similarity Percentage")
    plt.ylabel('Similarity Percentage',
               fontsize=12, fontweight='bold')
    plt.xlabel('Number of UAVs', fontsize=12, fontweight='bold')
    plt.title('Similarity percentage Vs Number of UAVs',
              fontsize=12, fontweight='bold')
    plt.xticks(fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    plt.legend()
    file_name = 'SimiPerctNewPlot.png'
    file_path = os.path.join(parent_dir, dir_name, file_name)
    # plt.savefig(file_path)
    plt.show()
    
    
def all_plot(data1, data2, data3):
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'GUNewPlot.png'
    file_path = os.path.join(parent_dir, dir_name, file_name)
    x_val = [key for key in data1]
    ground_user_covered = [value[0] for key, value in data1.items()]
    plt.scatter(x_val, ground_user_covered)
    plt.plot(x_val, ground_user_covered, label="Ground User served 100")
    ground_user_covered = [value[0] for key, value in data2.items()]
    plt.scatter(x_val, ground_user_covered)
    plt.plot(x_val, ground_user_covered, label="Ground User served 200")
    ground_user_covered = [value[0] for key, value in data3.items()]
    plt.scatter(x_val, ground_user_covered)
    plt.plot(x_val, ground_user_covered, label="Ground User served 300")
    plt.ylabel('Percentage of Ground User covered',
               fontsize=12, fontweight='bold')
    plt.xlabel('Number of UAVs', fontsize=12, fontweight='bold')
    plt.title('User coverage percentage Vs Number of UAVs',
              fontsize=12, fontweight='bold')
    plt.xticks(fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    plt.legend()
    # plt.savefig(file_path)
    plt.show()
    # Clear plot
    # plt.clf()
    # # Similarity Percentage
    similarity_percentage = [value[1] for key, value in data1.items()]
    plt.scatter(x_val, similarity_percentage)
    plt.plot(x_val, similarity_percentage, label="Similarity Percentage 100")
    similarity_percentage = [value[1] for key, value in data2.items()]
    plt.scatter(x_val, similarity_percentage)
    plt.plot(x_val, similarity_percentage, label="Similarity Percentage 300")
    similarity_percentage = [value[1] for key, value in data3.items()]
    plt.scatter(x_val, similarity_percentage)
    plt.plot(x_val, similarity_percentage, label="Similarity Percentage 300")
    plt.ylabel('Similarity Percentage',
               fontsize=12, fontweight='bold')
    plt.xlabel('Number of UAVs', fontsize=12, fontweight='bold')
    plt.title('Similarity percentage Vs Number of UAVs',
              fontsize=12, fontweight='bold')
    plt.xticks(fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    plt.legend()
    file_name = 'SimiPerctNewPlot.png'
    file_path = os.path.join(parent_dir, dir_name, file_name)
    # plt.savefig(file_path)
    plt.show()


def write_to_json(data, file_path):
    """
    Function: write_to_json\n
    Parameters: data -> data to be written, file_path -> path of the file\n
    Functionality: Writes the json data to the file\n
    """
    with open(file_path, 'w') as file_pointer:
        json.dump(data, file_pointer)


def init():
    """
    Function: init\n
    Parameter: None\n
    Functionality: Initializes the environment\n
    """
    global number_UAVs
    graph_data = {}
    os.system('bash fresh_analysis.sh')
    parent_dir = os.getcwd()
    target_dir = 'input_files'
    file_name = 'user_location.json'
    file_path = os.path.join(parent_dir, target_dir, file_name)
    with open(file_path, 'r') as file_pointer:
        data = json.load(file_pointer)
    number_users = data['Number of User'] / 100
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
        graph_data[number_UAV] = get_grounduser_and_similarity(number_users)
    file_path = os.path.join(
        os.getcwd(), 'analysis_output_files', 'GU_Similarity_plot.json')
    write_to_json(graph_data, file_path)
    line_plot(graph_data)


if __name__ == "__main__":
    dir_path = os.path.join(os.getcwd(), 'analysis_output_files')
    try:
        os.mkdir(dir_path)
    except OSError as error:
        pass
    # init()
    data_100 = {"10": [75.0, 12.5], "20": [95.0, 63.04347826086957], "30": [97.0, 77.21518987341773], "40": [99.0, 83.1858407079646], "50": [100.0, 85.62573099415205], "60": [100.0, 88.9344262295082], "70": [100.0, 91.3907284768212], "80": [100.0, 92.71708683473389], "90": [100.0, 93.54838709677419], "100": [100.0, 92.92035398230088]}
    data_200 = {"10": [70.5, 10.5], "20": [94.0, 45.65217391304348], "30": [97.0, 60.75949367088608], "40": [98.5, 66.3716814159292], "50": [99.9, 71.9298245614035], "60": [100.0, 74.90163934426229], "70": [100.0, 80.4635761589404], "80": [100.0, 84.03361344537815], "90": [100.0, 87.09677419354838], "100": [100.0, 90.04424778761062]}
    data_300 = {"10": [64.33333333333333, 6.25], "20": [84.0, 39.130434782608695], "30": [94.0, 57.29113924050633], "40": [96.66666666666667, 63.716814159292035], "50": [98.33333333333333, 66.51461988304094], "60": [100.0, 73.08196721311475], "70": [100.0, 79.13907284768213], "80": [100.0, 82.91316526610645], "90": [100.0, 85.60794044665012], "100": [100.0, 87.38938053097345]}
    # line_plot(data_100)
    # line_plot(data_200)
    # line_plot(data_300)
    all_plot(data_100, data_200, data_300)


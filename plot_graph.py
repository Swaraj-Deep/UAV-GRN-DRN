import os
import os.path
import matplotlib.pyplot as plt


def get_points():
    """
    Function: get_points\n
    Parameters: None\n
    Returns: list of tuples containing coordinate points\n
    """
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'scenario_analysis.log'
    file_path = os.path.join(parent_dir, dir_name, file_name)
    x = []
    y = []
    data = []
    with open(file_path, 'r') as file_pointer:
        data = file_pointer.readlines()
    for point in data[3:-3]:
        a = float(point.split(' ')[0])
        b = float(point.split(' ')[1])
        x.append(a)
        y.append(b)
    return (x, y)


def scatter_plot():
    """
    Function: scatter_plot\n
    Parameters: None\n
    Functionality: Plots graph for log generated from analyse_scenario.py python file\n
    """
    parent_dir = os.getcwd()
    dir_path = os.path.join(parent_dir, 'analysis_output_files')
    try:
        os.mkdir(dir_path)
    except OSError as error:
        pass
    y, x = get_points()
    plt.scatter(x, y)
    plt.title('UAV Communication Threshold vs Standard Deviation of User Distance')
    plt.xlabel('Standard Deviation of User Distance')
    plt.ylabel('UAV Communication Threshold')
    file_path = os.path.join(dir_path, 'scenario_analysis.png')
    plt.savefig(file_path)


def decide_to_plot():
    """
    Funciton: decide_to_plot\n
    Parameters: None\n
    Functionality: Decide what to plot according to the scenario_analysis.log file
    """
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'scenario_analysis.log'
    file_path = os.path.join(parent_dir, dir_name, file_name)
    lines = []
    with open(file_path, 'r') as file_pointer:
        lines = file_pointer.readlines()
    if len(lines[3:][0].split(' ')) > 2:
        bar_plot()
    else:
        scatter_plot()


def bar_plot():
    """
    Function: bar_plot\n
    Parameters: None\n
    Functionality: Read the data from the scenario_analysis.log file
    """
    graph_data = read_data()
    area = [item['Area'] for item in graph_data]
    UAV = [item['UAV'] for item in graph_data]
    user = [item['user'] for item in graph_data]
    similarity = [item['similarity'] for item in graph_data]
    std = [item['std'] for item in graph_data]
    comm_th = [item['comm_th'] for item in graph_data]


def read_data():
    """
    Function: read_data\n
    Parameters: None\n
    Functionality: Read the data and convert it to a meaning ful form\n
    """
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'scenario_analysis.log'
    file_path = os.path.join(parent_dir, dir_name, file_name)
    lines = []
    with open(file_path, 'r') as file_pointer:
        lines = file_pointer.readlines()
    data = lines[3:-3]
    graph_data_lst = []
    prev = 0
    for idx in range(0, len(data) + 1, 6):
        block_dict = {}
        block = data[prev:idx:]
        if len(block) > 1:
            block_dict['Area'] = block[0].split(':')[1].split('X')[0]
            block_dict['UAV'] = round(float(block[1].split(':')[1]), 2)
            block_dict['user'] = round(float(block[2].split(':')[1]), 2)
            block_dict['similarity'] = round(float(block[3].split(':')[1]), 2)
            block_dict['std'] = round(float(block[4].split(':')[1]), 2)
            block_dict['comm_th'] = round(float(block[5].split(':')[1]), 2)
            graph_data_lst.append(block_dict)
        prev = idx
    return graph_data_lst


if __name__ == "__main__":
    # scatter_plot()
    decide_to_plot()

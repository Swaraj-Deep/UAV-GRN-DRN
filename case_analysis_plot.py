import os
import os.path
import matplotlib.pyplot as plt
import json
import time
import pandas as pd

# Global Declarations
# Dictionary containing graph value
# Key is the point in x axis and value is a dictionary containing list of y values for different similarity thresholds
graph_data = {}
# The value dictionary of graph_data
helper_dict = {}


# list for similarity thresholds
sim_thld_lst = []

# Plot title
plot_title = ''

# X label
x_label = ''

# Y label
y_label = ''

# Maximum Iteration
max_iter = 5

# Running command

command = 'python3'
user_generation_script = 'user_secnario_producer.py'


def set_to_defaults():
    """
    Function: set_to_defaults\n
    Parameters: None\n
    Functionality: Sets the scenario_input.json and user_location.json file to default values.\n
    """
    parent_dir = os.getcwd()
    dir_name = 'input_files'
    file_path = os.path.join(parent_dir, dir_name)
    default_scenario = {}
    file_name = 'default_scenario.json'
    with open(os.path.join(file_path, file_name), 'r') as file_pointer:
        default_scenario = json.load(file_pointer)
    number_users = default_scenario['number_users']
    N = default_scenario['N']
    M = default_scenario['M']
    default_scenario.pop('number_users')
    file_name = 'scenario_input.json'
    with open(os.path.join(file_path, file_name), 'w') as file_pointer:
        json.dump(default_scenario, file_pointer)
    user_loc = {"N": N, "M": M, "Number of User": number_users}
    file_name = 'user_location.json'
    with open(os.path.join(file_path, file_name), 'w') as file_pointer:
        json.dump(user_loc, file_pointer)


def take_input():
    """
    Function: take_input\n
    Parameters: None\n
    Functionality: decide which graph to plot according to plot_input.json file\n
    """
    global sim_thld_lst, plot_title, x_label, y_label
    set_to_defaults()
    parent_dir = os.getcwd()
    dir_name = 'input_files'
    file_path = os.path.join(parent_dir, dir_name)
    plot_input_data = {}
    file_name = 'plot_input.json'
    with open(os.path.join(file_path, file_name), 'r') as file_pointer:
        plot_input_data = json.load(file_pointer)
    sim_thld_lst = plot_input_data['Similarity Threshold']
    plot_title = plot_input_data['plot_name']
    x_label = plot_input_data['x_axis']
    y_label = plot_input_data['y_axis']
    lst_to_iterate = plot_input_data[x_label]
    determine(lst_to_iterate)


def determine(lst_to_iterate):
    """
    Function: determine\n
    Parameters: lst_to_iterate -> list over which x axis value will depend\n
    Functionality: Determine x axis iterator\n
    """
    global x_label, sim_thld_lst
    if 'coverage' in x_label.lower():
        plot('coverage_threshold', lst_to_iterate)
    elif 'users' in x_label.lower():
        plot('Number of User', lst_to_iterate)
    elif 'area' in x_label.lower():
        plot('NM', lst_to_iterate)
    elif 'radius' in x_label.lower():
        plot('radius_UAV', lst_to_iterate)


def plot(type, lst_to_iterate):
    """
    Function: plot\n
    Parameter: type -> which plot to plot (^_^), lst_to_iterate -> list of data which will be changing \n
    Functionality: Create the plot of desiered type\n
    """
    global sim_thld_lst, command, user_generation_script, helper_dict
    parent_dir = os.getcwd()
    dir_name = 'input_files'
    file_path = os.path.join(parent_dir, dir_name)
    if type == 'Number of User':
        for iter in range(max_iter):
            for i in range(len(lst_to_iterate)):
                value = lst_to_iterate[i]
                diff = 0
                file_name = 'user_location.json'
                user_loc = {}
                user_input = {}
                with open(os.path.join(file_path, file_name), 'r') as file_pointer:
                    user_loc = json.load(file_pointer)
                if i != 0:
                    diff = value - lst_to_iterate[i - 1]
                    user_loc[type] = diff
                    file_name = 'user_input.json'
                    with open(os.path.join(file_path, file_name), 'r') as file_pointer:
                        user_input = json.load(file_pointer)
                    prev_user_pos = user_input['Position of Ground users']
                    file_name = 'user_location.json'
                    with open(os.path.join(file_path, file_name), 'w') as file_pointer:
                        json.dump(user_loc, file_pointer)
                    os.system(f'{command} {user_generation_script}')
                    file_name = 'user_input.json'
                    with open(os.path.join(file_path, file_name), 'r') as file_pointer:
                        user_input = json.load(file_pointer)
                    new_user_pos = user_input['Position of Ground users']
                    user_input['Number of Ground users'] = value
                    user_input['Position of Ground users'] = prev_user_pos + \
                        new_user_pos
                    with open(os.path.join(file_path, file_name), 'w') as file_pointer:
                        json.dump(user_input, file_pointer)
                else:
                    user_loc[type] = value
                    with open(os.path.join(file_path, file_name), 'w') as file_pointer:
                        json.dump(user_loc, file_pointer)
                    os.system(f'{command} {user_generation_script}')
                file_name = 'user_location.json'
                user_loc[type] = value
                with open(os.path.join(file_path, file_name), 'w') as file_pointer:
                    json.dump(user_loc, file_pointer)
                for similarity_threshold in sim_thld_lst:
                    file_name = 'scenario_input.json'
                    scenario_data = {}
                    with open(os.path.join(file_path, file_name), 'r') as file_pointer:
                        scenario_data = json.load(file_pointer)
                    scenario_data['similarity_threshold'] = similarity_threshold
                    with open(os.path.join(file_path, file_name), 'w') as file_pointer:
                        json.dump(scenario_data, file_pointer)
                    os.system(f'{command} main.py')
                    os.system(f'{command} analysis.py')
                    update_file(similarity_threshold,
                                value, get_number_UAV())
                    os.system('bash fresh_analysis.sh')
        plot_graph(True)
    elif type == 'NM':
        for value in lst_to_iterate:
            helper_dict = {}
            N, M = map(int, value.split(' '))
            file_name = 'user_location.json'
            user_loc = {}
            with open(os.path.join(file_path, file_name), 'r') as file_pointer:
                user_loc = json.load(file_pointer)
            user_loc['N'] = N
            user_loc['M'] = M
            with open(os.path.join(file_path, file_name), 'w') as file_pointer:
                json.dump(user_loc, file_pointer)
            for iter in range(max_iter):
                os.system(f'{command} {user_generation_script}')
                for similarity_threshold in sim_thld_lst:
                    file_name = 'scenario_input.json'
                    scenario_data = {}
                    with open(os.path.join(file_path, file_name), 'r') as file_pointer:
                        scenario_data = json.load(file_pointer)
                    scenario_data['similarity_threshold'] = similarity_threshold
                    with open(os.path.join(file_path, file_name), 'w') as file_pointer:
                        json.dump(scenario_data, file_pointer)
                    os.system(f'{command} main.py')
                    os.system(f'{command} analysis.py')
                    update_file(similarity_threshold,
                                value, get_number_UAV())
                    os.system('bash fresh_analysis.sh')
        plot_graph(False)
    else:
        for value in lst_to_iterate:
            helper_dict = {}
            for iter in range(max_iter):
                os.system(f'{command} {user_generation_script}')
                for similarity_threshold in sim_thld_lst:
                    file_name = 'scenario_input.json'
                    scenario_data = {}
                    with open(os.path.join(file_path, file_name), 'r') as file_pointer:
                        scenario_data = json.load(file_pointer)
                    scenario_data['similarity_threshold'] = similarity_threshold
                    scenario_data[type] = value
                    with open(os.path.join(file_path, file_name), 'w') as file_pointer:
                        json.dump(scenario_data, file_pointer)
                    os.system(f'{command} main.py')
                    os.system(f'{command} analysis.py')
                    update_file(similarity_threshold,
                                value, get_number_UAV())
                    os.system('bash fresh_analysis.sh')
        plot_graph(True)


def update_file(similarity_threshold, x_data, y_data):
    """
    Function update_file\n
    Parameters: similarity_threshold, x_data -> data point on x axis, y_data -> data point on y axis\n
    Functionality: Updates the file with required Parameters\n
    """
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'graph_data.log'
    line_to_write = f'{similarity_threshold} {x_data} {y_data}\n'
    with open(os.path.join(parent_dir, dir_name, file_name), 'a') as file_pointer:
        file_pointer.writelines(line_to_write)


def get_number_UAV():
    """
    Function: get_number_UAV\n
    Parameters: None\n
    Returns: Number of UAVs required to reach that target\n
    """
    parent_dir = os.getcwd()
    dir_name = 'input_files'
    file_path = os.path.join(parent_dir, dir_name)
    scenario_input = {}
    file_name = 'scenario_input.json'
    with open(os.path.join(file_path, file_name), 'r') as file_pointer:
        scenario_input = json.load(file_pointer)
    epsilon = scenario_input['epsilon']
    learning_rate = scenario_input['learning_rate']
    decay_factor = scenario_input['decay_factor']
    parent_dir = os.path.join(os.getcwd(), 'output_files')
    curr_dir = str(epsilon) + "_" + str(learning_rate) + \
        "_" + str(decay_factor)
    dir_path = os.path.join(parent_dir, curr_dir)
    file_name = 'analysis.log'
    file_data = []
    with open(os.path.join(dir_path, file_name), 'r') as file_pointer:
        file_data = file_pointer.readlines()
    line_number = 13
    return int(float(file_data[line_number].split(':')[1]))


def process_graph_data():
    """
    Function: process_graph_data\n
    Parameter: None\n
    Functionality: Process the graph_data to make it ready for plots\n
    Returns: dictionary where key is similarity_threshold and value is a list where each list item contains a tuple of x_point and a list of y_point where list items are 75%, std, mean, min, max, median\n
    """
    global graph_data
    processed_data = {}
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'graph_data.log'
    data = []
    with open(os.path.join(parent_dir, dir_name, file_name), 'r') as file_pointer:
        data = file_pointer.readlines()
    data = data[1:]
    for line in data:
        lst_temp = line.split(' ')
        if len(lst_temp) == 4:
            sim_th = round(float(lst_temp[0]), 2)
            N = round(float(lst_temp[1]), 2)
            M = round(float(lst_temp[2]), 2)
            x_data = (N, M)
            y_data = round(float(lst_temp[3]), 2)
        else:    
            sim_th = round(float(lst_temp[0]), 2)
            x_data = round(float(lst_temp[1]), 2)
            y_data = float(lst_temp[2])
        key = (sim_th, x_data)
        if key not in processed_data:
            processed_data[key] = [y_data]
        else:
            processed_data[key].append(y_data)
    for key, y_lst in processed_data.items():
        temp_df = pd.DataFrame(y_lst)
        des_dict = temp_df.describe()[0]
        output_lst = [round(float(des_dict['75%']), 2), round(float(des_dict['std']), 2), round(float(des_dict['mean']), 2), round(float(des_dict['min']), 2), round(float(des_dict['max']), 2), round(float(des_dict['50%']), 2)]
        sim_th, x_data = key
        if sim_th not in graph_data:
            graph_data[sim_th] = [(x_data, output_lst)]
        else:
            graph_data[sim_th].append((x_data, output_lst))
    return graph_data


def plot_graph(flag):
    """
    Function: plot_graph\n
    Parameter: flag -> bool variable to indicate the type of plot\n
    Functionality: Generate the plot\n
    """
    global graph_data, plot_title, x_label, y_label
    graph_data = process_graph_data()
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'graph_data.json'
    with open(os.path.join(parent_dir, dir_name, file_name), 'w') as file_pointer:
        json.dump(graph_data, file_pointer)
    if flag:
        for sim_thld, points in graph_data.items():
            x = []
            y = []
            for point in points:
                a, b = point
                x.append(a)
                y.append(b[0])
            plt.scatter(x, y)
            plt.plot(x, y, label=f'{sim_thld}')
    else:
        parent_dir = os.getcwd()
        dir_name = 'input_files'
        file_name = 'scenario_input.json'
        scenario_data = {}
        with open(os.path.join(parent_dir, dir_name, file_name), 'r') as file_pointer:
            scenario_data = json.load(file_pointer)
        cell_size = scenario_data['cell_size']
        unit_mul = scenario_data['unit_multiplier']
        cell_size *= unit_mul
        cell_size = unit_mul / cell_size
        for sim_thld, points in graph_data.items():
            x = []
            y = []
            for point in points:
                x_data, y_data = point
                N, M = map(int, x_data)
                x.append(f'{N // cell_size} X {M // cell_size}')
                y.append(y_data[0])
            plt.scatter(x, y)
            plt.plot(x, y, label=f'{sim_thld}')
    plt.title(
        plot_title, fontweight="bold")
    plt.xlabel(x_label, fontweight='bold')
    plt.ylabel(y_label, fontweight='bold')
    plt.legend()
    file_name = f'{plot_title}'
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    plt.savefig(os.path.join(parent_dir, dir_name, file_name))


if __name__ == "__main__":
    dir_path = os.path.join(os.getcwd(), 'analysis_output_files')
    try:
        os.mkdir(dir_path)
    except OSError as error:
        pass
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'graph_data.log'
    line_to_write = f'+-----------------------------Data-----------------------------+\n'
    with open (os.path.join (parent_dir, dir_name, file_name), 'w') as file_pointer:
        file_pointer.writelines(line_to_write)
    os.system('bash fresh_analysis.sh')
    print(f'Relax!! we have taken the charge. (-_-)')
    os.system('bash fresh_analysis.sh')
    take_input()

import os
import os.path
import matplotlib.pyplot as plt
import json

# Global Declarations
# Dictionary containing graph value
graph_data = {}

# list for similarity thresholds
sim_thld_lst = []

# Plot title
plot_title = ''

# X label
x_label = ''

# Y label
y_label = ''

# Maximum Iteration
max_iter = 1


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
    elif 'ground' in x_label.lower():
        plot('Number of User', lst_to_iterate)
    elif 'area' in x_label.lower():
        plot('NM', lst_to_iterate)
    elif 'radius' in x_label.lower():
        plot('UAV_to_UAV_threshold', lst_to_iterate)


def plot(type, lst_to_iterate):
    """
    Function: plot\n
    Parameter: type -> which plot to plot ^_^, lst_to_iterate -> list of data which will be changing \n
    Functionality: Create the plot of desiered type\n
    """
    global sim_thld_lst
    parent_dir = os.getcwd()
    dir_name = 'input_files'
    file_path = os.path.join(parent_dir, dir_name)
    if type == 'Number of User':
        for similarity_threshold in sim_thld_lst:
            file_name = 'scenario_input.json'
            scenario_data = {}
            with open(os.path.join(file_path, file_name), 'r') as file_pointer:
                scenario_data = json.load(file_pointer)
            scenario_data['similarity_threshold'] = similarity_threshold
            with open(os.path.join(file_path, file_name), 'w') as file_pointer:
                json.dump(scenario_data, file_pointer)
            for value in lst_to_iterate:
                file_name = 'user_location.json'
                user_loc = {}
                with open(os.path.join(file_path, file_name), 'r') as file_pointer:
                    user_loc = json.load(file_pointer)
                user_loc[type] = value
                with open(os.path.join(file_path, file_name), 'w') as file_pointer:
                    json.dump(user_loc, file_pointer)
                execute()
                update_dictionary(similarity_threshold, value)
                os.system('bash fresh_analysis.sh')
        plot_graph(True)
    elif type == 'NM':
        for similarity_threshold in sim_thld_lst:
            file_name = 'scenario_input.json'
            scenario_data = {}
            with open(os.path.join(file_path, file_name), 'r') as file_pointer:
                scenario_data = json.load(file_pointer)
            scenario_data['similarity_threshold'] = similarity_threshold
            with open(os.path.join(file_path, file_name), 'w') as file_pointer:
                json.dump(scenario_data, file_pointer)
            for value in lst_to_iterate:
                N, M = map(int, value.split(' '))
                file_name = 'user_location.json'
                user_loc = {}
                with open(os.path.join(file_path, file_name), 'r') as file_pointer:
                    user_loc = json.load(file_pointer)
                user_loc['N'] = N
                user_loc['M'] = M
                with open(os.path.join(file_path, file_name), 'w') as file_pointer:
                    json.dump(user_loc, file_pointer)
                execute()
                update_dictionary(similarity_threshold, (N, M))
        plot_graph(False)
    else:
        for similarity_threshold in sim_thld_lst:
            for value in lst_to_iterate:
                file_name = 'scenario_input.json'
                scenario_data = {}
                with open(os.path.join(file_path, file_name), 'r') as file_pointer:
                    scenario_data = json.load(file_pointer)
                scenario_data['similarity_threshold'] = similarity_threshold
                scenario_data[type] = value
                with open(os.path.join(file_path, file_name), 'w') as file_pointer:
                    json.dump(scenario_data, file_pointer)
                execute()
                update_dictionary(similarity_threshold, value)
                os.system('bash fresh_analysis.sh')
        plot_graph(True)


def update_dictionary(similarity_threshold, x_data):
    """
    Function update_dictionary\n
    Parameters: similarity_threshold, x_data -> data point on x axis\n
    Functionality: Updates the dictionary with required Parameters\n
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
    line_number = get_line_number(file_data)
    y_data = int(float(file_data[line_number].split(':')[1]))
    global graph_data
    if similarity_threshold in graph_data:
        graph_data[similarity_threshold].append((x_data, y_data))
    else:
        graph_data[similarity_threshold] = [(x_data, y_data)]


def get_line_number(file_data):
    """
    Function: get_line_number\n
    Parameters: file_data -> list of lines in the file\n
    """
    return 13


def execute():
    """
    Function excute\n
    Parameters: None\n
    Functionality: Executes main.py given number of times\n
    """
    for iter in range(max_iter):
        os.system('python3 user_scenario_cluster.py')
        os.system('python3 main.py')
    os.system('python3 analysis.py')


def plot_graph(flag):
    """
    Function: plot_graph\n
    Parameter: flag -> bool variable to indicate the type of plot\n
    Functionality: Generate the plot\n
    """
    global graph_data, plot_title, x_label, y_label
    if flag:
        for sim_thld, points in graph_data.items():
            x = []
            y = []
            for point in points:
                a, b = point
                x.append(a)
                y.append(b)
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
                N, M = x_data
                x.append(f'{N // cell_size} X {M // cell_size}')
                y.append(y_data)
            plt.scatter(x, y)
            plt.plot(x, y, label=f'{sim_thld}')
    plt.title(
        plot_title, fontweight="bold")
    plt.xlabel(x_label, fontweight='bold')
    plt.ylabel(y_label, fontweight='bold')
    plt.legend()
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = f'{plot_title}'
    plt.savefig(os.path.join(parent_dir, dir_name, file_name))
    file_name = 'graph_data.json'
    with open(os.path.join(parent_dir, dir_name, file_name), 'w') as file_pointer:
        json.dump(graph_data, file_pointer)


if __name__ == "__main__":
    dir_path = os.path.join(os.getcwd(), 'analysis_output_files')
    try:
        os.mkdir(dir_path)
    except OSError as error:
        pass
    print(f'Relax!! we have taken the charge. ^_^')
    os.system('bash fresh_analysis.sh')
    take_input()

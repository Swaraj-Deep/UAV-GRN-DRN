import os
import os.path
import json

# Global Declarations
# list for similarity thresholds
sim_thld_lst = []

# Plot title
plot_title = ''

# X label
x_label = ''

# Y label
y_label = ''

# Maximum Iteration
max_iter = 0


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
    global sim_thld_lst, x_label, y_label, plot_title
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
            scenario_data[type] = value
            with open(os.path.join(file_path, file_name), 'w') as file_pointer:
                json.dump(scenario_data, file_pointer)
            for value in lst_to_iterate:
                file_name = 'user_location.json'

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
                os.system('python3 user_scenario_cluster.py')
                os.system('python3 main.py')


take_input()

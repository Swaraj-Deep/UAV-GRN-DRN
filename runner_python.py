import os
import json
from sys import platform

epsilon_vals_list = [0.7, 0.71]
# [, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 0.81, 0.82,
#                      0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99]

learning_rate_list = [0.8, 0.81, 0.82]
# , 0.83, 0.84, 0.85, 0.86, 0.87,
#                       0.88, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99]

decay_factor_list = [0.90, 0.91]
# , 0.92, 0.93,
#                      0.94, 0.95, 0.96, 0.97, 0.98, 0.99]


def execute_file():
    dir = os.getcwd()
    if platform == "linux" or platform == "linux2":
        file_loc = os.path.join (dir, 'runner.sh')
        os.system(file_loc)
    elif platform == "darwin":
        # I don't have Mac
        pass
    elif platform == "win32":
        file_loc = os.path.join (dir, 'runner.bat')
        os.system(file_loc)


def change_scenario_input():
    for epsilon in epsilon_vals_list:
        for learning_rate in learning_rate_list:
            for deacy_factor in decay_factor_list:
                file_data = ''
                with open('input_files/scenario_input.json', 'r') as file_pointer:
                    file_data = json.load(file_pointer)
                file_data["learning_rate"] = learning_rate
                file_data["epsilon"] = epsilon
                file_data["decay_factor"] = deacy_factor
                with open('input_files/scenario_input.json', 'w') as file_pointer:
                    json.dump(file_data, file_pointer)
                execute_file()


if __name__ == "__main__":
    change_scenario_input()
    os.system('python3 analysis_best_from_output.py')

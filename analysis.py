import os
import json
import os.path


def analyse_output_files():
    """
    Function: analyse_output_files\n
    Functionality: Calculate the mean of the output files, provides the best and the worst output files\n
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
    curr_dir = str(epsilon) + "_" + str(learning_rate) + "_" + str(decay_factor)
    dir_path = os.path.join (parent_dir, curr_dir)
    # os.chdir(dir_path)
    text_files = []
    minm_user_served = 999999999
    maxm_user_served = -99999999
    curr_user_served = 0
    worst_file = ''
    best_file = ''
    sum_user_served = 0
    total_files = 0
    for file in os.listdir(dir_path):
        name, ext = os.path.splitext(file)
        if ext == '.txt':
            text_files.append(name + ext)
            total_files += 1
    for file in text_files:
        with open(dir_path + "/" + file, 'r') as file_pointer:
            lines = file_pointer.readlines()
            curr_user_served = int(lines[-2].split(':')[1])
            sum_user_served += curr_user_served
            if curr_user_served < minm_user_served:
                minm_user_served = curr_user_served
                worst_file = dir_path + "/" + file
            if curr_user_served > maxm_user_served:
                maxm_user_served = curr_user_served
                best_file = dir_path + "/" + file
    list_line_to_write = []
    list_line_to_write.append(f'############################################################################################\n')
    list_line_to_write.append(f'################################### Analysis Report ########################################\n')
    list_line_to_write.append(f'############################################################################################\n')
    best_graph = dir_path + '/Output_graph' + \
        best_file[26:len(best_file) - 4:] + '.png'
    list_line_to_write.append(f'# Location of Best Output file is: {best_file}\n')
    list_line_to_write.append(f'# Corresponding Graph file location is: {best_graph}\n')
    worst_graph = dir_path + '/Output_graph' + \
        worst_file[26:len(worst_file) - 4:] + '.png'
    list_line_to_write.append(
        f'# Location of Worst Output file is: {worst_file}\n')
    list_line_to_write.append(f'# Corresponding Graph file location is: {worst_graph}\n')
    list_line_to_write.append(f'# Mean User Served: {sum_user_served / total_files}\n')
    list_line_to_write.append("############################################################################################\n")
    with open(dir_path + "/" + "analysis.log", 'w') as file_pointer:
        file_pointer.writelines(list_line_to_write)


if __name__ == "__main__":
    analyse_output_files()

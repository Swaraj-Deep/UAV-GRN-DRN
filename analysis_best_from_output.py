import os
import json
import os.path


def get_file_details(file_name):
    """
    Function: get_file_details\n
    parameter: file_name -> name of the file to be analysed\n
    return: dict containing max and min user served\n
    """
    ret_dict = {}
    with open(file_name) as file_pointer:
        lines = file_pointer.readlines()
        ret_dict["Learning Rate"] = float(lines[1].split(":")[1])
        ret_dict["Exploration Rate"] = float(lines[2].split(":")[1])
        ret_dict["Decay Factor"] = float(lines[3].split(":")[1])
        ret_dict["Best User Served"] = float(lines[-3].split(":")[1])
        ret_dict["Worst User Served"] = float(lines[-2].split(":")[1])
    return ret_dict


def analyse_output_files():
    """
    Function: analyse_output_files\n
    Functionality: Provide information about the best scenario\n
    """
    best_file_loc = ""
    worst_file_loc = ""
    best_user_cov = -9999999
    worst_user_cov = 9999999
    path = os.path.join(os.getcwd(), 'output_files')
    for dirs in os.listdir(path):
        dir_path = os.path.join(path, dirs)
        if os.path.isdir(dir_path):
            file_path = os.path.join(path, dirs)
            for file in os.listdir(file_path):
                if file == 'analysis.log':
                    full_file_path = os.path.join(file_path, file)
                    file_read_dict = get_file_details(full_file_path)
                    if file_read_dict['Best User Served'] > best_user_cov:
                        best_user_cov = file_read_dict['Best User Served']
                        best_file_loc = full_file_path
                    if file_read_dict['Worst User Served'] < worst_user_cov:
                        worst_user_cov = file_read_dict['Worst User Served']
                        worst_file_loc = full_file_path
    file_read_dict = get_file_details(best_file_loc)
    lines_to_write = []
    lines_to_write.append(
        f'############################################################################################\n')
    lines_to_write.append(
        f'############################### Overall Analysis Report ####################################\n')
    lines_to_write.append(
        f'############################################################################################\n')
    lines_to_write.append(
        f'# The best scenario turns out to be with following parameters\n# Learning Rate: {file_read_dict["Learning Rate"]}\n# Exploration Rate: {file_read_dict["Exploration Rate"]}\n# Decay Factor: {file_read_dict["Decay Factor"]}\n')
    lines_to_write.append(
        f'# The best file in this scenario can cover upto {file_read_dict["Best User Served"]} ground users\n                       while \n# In the worst case only {file_read_dict["Worst User Served"]} ground user can be served.\n')
    lines_to_write.append(f'# The best file of this scenario is: {best_file_loc}')
    file_read_dict = get_file_details(worst_file_loc)
    lines_to_write.append(
        f'# The worst scenario turns out to be with following parameters\n# Learning Rate: {file_read_dict["Learning Rate"]}\n# Exploration Rate: {file_read_dict["Exploration Rate"]}\n# Decay Factor: {file_read_dict["Decay Factor"]}\n')
    lines_to_write.append(
        f'# The best file in this scenario can cover upto {file_read_dict["Best User Served"]} ground users\n                       while \n# In the worst case only {file_read_dict["Worst User Served"]} ground user can be served.\n')
    lines_to_write.append(f'# The worst file of this scenario is: {worst_file_loc}')
    lines_to_write.append(
        f'############################################################################################\n')
    dir_path = os.path.join(os.getcwd(), 'output_files')
    with open(os.path.join(dir_path, "overallanalysis.log"), 'w') as file_pointer:
        file_pointer.writelines(lines_to_write)


if __name__ == "__main__":
    analyse_output_files()

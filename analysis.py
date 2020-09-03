import os
import json
import os.path
import pandas as pd


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
    curr_dir = str(epsilon) + "_" + str(learning_rate) + \
        "_" + str(decay_factor)
    dir_path = os.path.join(parent_dir, curr_dir)
    text_files = []
    minm_user_served = 999999999
    maxm_user_served = -99999999
    curr_user_served = 0
    minm_UAV_used = 99999999999
    minm_sim = 99999999
    maxm_sim = -99999999
    curr_UAV_used = 0
    worst_file_sim_per = ''
    worst_file = ''
    best_file_sim_per = ''
    best_file = ''
    best_graph = ''
    best_graph_sim_per = ''
    worst_graph = ''
    worst_graph_sim_per = ''
    total_files = 0
    for file in os.listdir(dir_path):
        name, ext = os.path.splitext(file)
        if ext == '.txt':
            text_files.append(name + ext)
            total_files += 1
    lst_UAV = []
    lst_user = []
    lst_similarity = []
    lst_sd_distances_user = []
    for file in text_files:
        with open(os.path.join(dir_path, file), 'r') as file_pointer:
            lines = file_pointer.readlines()
            curr_user_served = int(lines[0].split(':')[1])
            curr_UAV_used = int(lines[2].split(':')[1])
            lst_sd_distances_user.append(float(lines[-2].split(':')[1]))
            similarity_percentage = float(
                find_percentage(lines, curr_UAV_used))
            lst_UAV.append(curr_UAV_used)
            lst_similarity.append(similarity_percentage)
            lst_user.append(curr_user_served)
            if curr_UAV_used < minm_UAV_used:
                if curr_user_served >= maxm_user_served:
                    maxm_user_served = curr_user_served
                    minm_UAV_used = curr_UAV_used
                    best_file = file
                    best_graph = file.split(
                        '_')[0] + '_graph' + file.split('_')[1][4:-4] + '.pdf'
            if curr_UAV_used > minm_UAV_used:
                if curr_user_served < minm_user_served:
                    minm_user_served = curr_user_served
                    worst_file = file
                    worst_graph = file.split(
                        '_')[0] + '_graph' + file.split('_')[1][4:-4] + '.pdf'
            if similarity_percentage > maxm_sim:
                maxm_sim = similarity_percentage
                best_file_sim_per = file
                best_graph_sim_per = file.split(
                    '_')[0] + '_graph' + file.split('_')[1][4:-4] + '.pdf'
            if similarity_percentage < minm_sim:
                minm_sim = similarity_percentage
                worst_file_sim_per = file
                worst_graph_sim_per = file.split(
                    '_')[0] + '_graph' + file.split('_')[1][4:-4] + '.pdf'

    best_file = os.path.join(dir_path, best_file)
    best_graph = os.path.join(dir_path, 'images', best_graph)
    worst_file = os.path.join(dir_path, worst_file)
    worst_graph = os.path.join(dir_path, 'images',  worst_graph)
    best_file_sim_per = os.path.join(dir_path, best_file_sim_per)
    best_graph_sim_per = os.path.join(dir_path, 'images',  best_graph_sim_per)
    worst_file_sim_per = os.path.join(dir_path, worst_file_sim_per)
    worst_graph_sim_per = os.path.join(dir_path,  'images', worst_graph_sim_per)

    df_UAV = pd.DataFrame(lst_UAV)
    df_user = pd.DataFrame(lst_user)
    df_similarity = pd.DataFrame(lst_similarity)
    df_sd_distances_user = pd.DataFrame(lst_sd_distances_user)

    desc_UAV = df_UAV.describe()
    desc_user = df_user.describe()
    desc_similarity = df_similarity.describe()

    mean_UAV = desc_UAV[0]['mean']
    std_UAV = desc_UAV[0]['std']
    min_UAV = desc_UAV[0]['min']
    median_UAV = desc_UAV[0]['50%']
    seventy_five_UAV = desc_UAV[0]['75%']
    max_UAV = desc_UAV[0]['max']
    mode_UAV = df_UAV.mode()
    mode_UAV = mode_UAV[0][len(mode_UAV) - 1]

    mean_user = desc_user[0]['mean']
    std_user = desc_user[0]['std']
    min_user = desc_user[0]['min']
    median_user = desc_user[0]['50%']
    seventy_five_user = desc_user[0]['75%']
    max_user = desc_user[0]['max']
    mode_user = df_user.mode()
    mode_user = mode_user[0][len(mode_user) - 1]

    mean_similarity = desc_similarity[0]['mean']
    std_similarity = desc_similarity[0]['std']
    min_similarity = desc_similarity[0]['min']
    median_similarity = desc_similarity[0]['50%']
    seventy_five_similarity = desc_similarity[0]['75%']
    max_similarity = desc_similarity[0]['max']
    mode_similarity = df_similarity.mode()
    mode_similarity = mode_similarity[0][len(mode_similarity) - 1]

    lines_to_write = []
    lines_to_write.append(
        f'Input Scenario\nEpsilon: {epsilon}\nLearning Rate: {learning_rate}\nDecay Factor: {decay_factor}\n')
    lines_to_write.append(
        f'############################################################################################\n')
    lines_to_write.append(
        f'################################### Analysis Report ########################################\n')
    lines_to_write.append(
        f'############################################################################################\n')
    lines_to_write.append(
        f'# Mean of UAVs: {mean_UAV}\n# Median of UAVs: {median_UAV}\n# Mode of UAVs: {mode_UAV}\n# Standard Deviation of UAVs: {std_UAV}\n# Minimum UAV used: {min_UAV}\n# Maximum UAV used: {max_UAV}\n# Seventy Five percentile of UAV: {seventy_five_UAV}\n')
    lines_to_write.append(
        f'# Mean of edge similarity: {mean_similarity}\n# Median of edge similarity: {median_similarity}\n# Mode of edge similarity: {mode_similarity}\n# Standard Deviation of edge similarity: {std_similarity}\n# Minimum edge similarity: {min_similarity}\n# Maximum edge similarity: {max_similarity}\n# Seventy Five percentile of edge similarity: {seventy_five_similarity}\n')
    lines_to_write.append(
        f'# Mean user served: {mean_user}\n# Median user served: {median_user}\n# Mode of user served: {mode_user}\n# Standard Deviation of user served: {std_user}\n# Minimum user served: {min_user}\n# Maximum user served: {max_user}\n# Seventy Five percentile of users: {seventy_five_user}\n')
    lines_to_write.append(
        f'# Seventy Five percentile of standard deviation of distance between users: {df_sd_distances_user.describe()[0]["75%"]}\n')
    lines_to_write.append(f'# Best File Location: {best_file}\n')
    lines_to_write.append(f'# Corresponding Graph Location: {best_graph}\n')
    if best_file_sim_per != best_file:
        lines_to_write.append(
            f'# Best File Location according to edge similarity: {best_file_sim_per}\n')
        lines_to_write.append(
            f'# Corresponding Graph Location: {best_graph_sim_per}\n')
    lines_to_write.append(f'# Worst File Location: {worst_file}\n')
    lines_to_write.append(f'# Corresponding Graph Location: {worst_graph}\n')
    if worst_file_sim_per != worst_file:
        lines_to_write.append(
            f'# Worst File Location according to edge similarity: {worst_file_sim_per}\n')
        lines_to_write.append(
            f'# Corresponding Graph Location: {worst_graph_sim_per}\n')
    lines_to_write.append(
        f'###############################################################################################\n')
    lines_to_write.append(
        f'###################################### END OF REPORT ##########################################\n')
    lines_to_write.append(
        f'###############################################################################################\n')
    with open(os.path.join(dir_path, "analysis.log"), 'w') as file_pointer:
        file_pointer.writelines(lines_to_write)


if __name__ == "__main__":
    analyse_output_files()

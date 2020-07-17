import os
import json
import os.path


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
    sum_user_served = 0
    sum_sim_per = 0
    total_files = 0
    for file in os.listdir(dir_path):
        name, ext = os.path.splitext(file)
        if ext == '.txt':
            text_files.append(name + ext)
            total_files += 1
    for file in text_files:
        with open(os.path.join(dir_path, file), 'r') as file_pointer:
            lines = file_pointer.readlines()
            curr_user_served = int(lines[0].split(':')[1])
            curr_UAV_used = int(lines[2].split(':')[1])
            sum_user_served += curr_user_served
            similarity_percentage = float(
                find_percentage(lines, curr_UAV_used))
            sum_sim_per += similarity_percentage
            if curr_UAV_used < minm_UAV_used:
                if curr_user_served >= maxm_user_served:
                    maxm_user_served = curr_user_served
                    minm_UAV_used = curr_UAV_used
                    best_file = file
            if curr_UAV_used > minm_UAV_used:
                if curr_user_served < minm_user_served:
                    minm_user_served = curr_user_served
                    worst_file = file

            if similarity_percentage > maxm_sim:
                maxm_sim = similarity_percentage
                best_file_sim_per = file
            if similarity_percentage < minm_sim:
                minm_sim = similarity_percentage
                worst_file_sim_per = file
    best_file = os.path.join(dir_path, best_file)
    worst_file = os.path.join(dir_path, worst_file)
    best_file_sim_per = os.path.join(dir_path, best_file_sim_per)
    worst_file_sim_per = os.path.join(dir_path, worst_file_sim_per)
    list_line_to_write = []
    list_line_to_write.append(
        f"Input Scenario\nLearning Rate: {learning_rate}\nExploration Rate: {epsilon}\nDecay Factor: {decay_factor}\n")
    list_line_to_write.append(
        f'############################################################################################\n')
    list_line_to_write.append(
        f'################################### Analysis Report ########################################\n')
    list_line_to_write.append(
        f'############################################################################################\n')
    best_graph = dir_path + '/Output_graph' + \
        best_file[26:len(best_file) - 4:] + '.png'
    list_line_to_write.append(
        f'Location of Best Output file is: {best_file}\n')
    list_line_to_write.append(
        f'Corresponding Graph file location is: {best_graph}\n')
    list_line_to_write.append(
        f'Location of Best Output file on the basis of edge similarity is: {best_file_sim_per}\n')
    best_graph_sim_per = dir_path + '/Output_graph' + \
        best_file_sim_per[26:len(best_file_sim_per) - 4:] + '.png'
    list_line_to_write.append(
        f'Corresponding Graph file location is: {best_graph_sim_per}\n')
    worst_graph = dir_path + '/Output_graph' + \
        worst_file[26:len(worst_file) - 4:] + '.png'
    list_line_to_write.append(
        f'Location of Worst Output file is: {worst_file}\n')
    list_line_to_write.append(
        f'Corresponding Graph file location is: {worst_graph}\n')
    list_line_to_write.append(
        f'Location of Worst Output file on the basis of edge similarity is: {worst_file_sim_per}\n')
    worst_graph_sim_per = dir_path + '/Output_graph' + \
        worst_file_sim_per[26:len(worst_file_sim_per) - 4:] + '.png'
    list_line_to_write.append(
        f'Corresponding Graph file location is: {worst_graph_sim_per}\n')
    list_line_to_write.append(
        f'Mean Edge Similarity: {sum_sim_per / total_files}\n')
    list_line_to_write.append(
        f'Edge Similarity in Best Case: {maxm_sim} \n')
    list_line_to_write.append(
        f'Edge Similarity in Worst Case: {minm_sim} \n')
    list_line_to_write.append(
        f'Mean User Served: {sum_user_served / total_files}\n')
    list_line_to_write.append(
        f'User Served in Best Case: {maxm_user_served} \n')
    list_line_to_write.append(
        f'User Served in Worst Case: {minm_user_served} \n')
    list_line_to_write.append(
        f"############################################################################################\n")
    with open(os.path.join(dir_path, "analysis.log"), 'w') as file_pointer:
        file_pointer.writelines(list_line_to_write)


if __name__ == "__main__":
    analyse_output_files()

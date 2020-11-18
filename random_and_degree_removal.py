import os
import json
import targeted_removal_endpoints.targeted_degree as targeted_degree
import targeted_removal_endpoints.targeted_random as targeted_random

# Command python or python3

command = "python3"

# User generation Script

script = "user_secnario_producer.py"

def filter_file_names():
    """
    Function: filter_file_names\n
    Parameter: None\n
    Functionality: Run the sumilations and return a dict of file names\n
    """
    os.system(f'bash fresh_analysis.sh')
    os.system(f'{command} {script}')
    os.system(f'{command} baseline.py')
    os.system(f'{command} main.py')
    file_names = {}
    for file in os.listdir(os.path.join(os.getcwd(), 'graph_output_files')):
        last_name = file.split('.')[0].split('_')[1]
        if 'baseline' in last_name:
            number = int(last_name[8:])
            if number in file_names:
                file_names[number].append(file)
            else:
                file_names[number] = [file]
        else:
            number = int(last_name[4:])
            if number in file_names:
                file_names[number].append(file)
            else:
                file_names[number] = [file]
    return file_names


def init():
    """
    Function: init\n
    Parameter: None\n
    Functionality: Targeted Random and degree removal\n
    """
    file_names = filter_file_names()
    lst_file_names = sorted(file_names[0])
    targeted_degree.init(lst_file_names[0], lst_file_names[1])
    # targeted_random.init(lst_file_names[0], lst_file_names[1])


if __name__ == "__main__":
    dir_path = os.path.join(os.getcwd(), 'analysis_output_files')
    try:
        os.mkdir(dir_path)
    except OSError as error:
        pass
    dir_path = os.path.join(os.getcwd(), 'node_failures_plots')
    try:
        os.mkdir(dir_path)
    except OSError as error:
        pass
    print(f'Relax!! we have taken the charge. (-_-)')
    init()

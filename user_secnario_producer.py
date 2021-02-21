import os.path
import random
import json
import os
import matplotlib.pyplot as plt


def generate_user_input(N, M, number_users):
    """
    Function: generate_user_input\n
    Parameter: (N, M) -> size of the grid, number_users -> Number of ground user needed to be placed\n
    Returns: nothing\n
    Functionality: Writes the output to user_input file and update scenario file\n
    """
    user_pos = []
    while len(user_pos) < number_users:
        a = round(random.uniform(0, N - 1), 2)
        b = round(random.uniform(0, M - 1), 2)
        if str(a) + " " + str(b) not in user_pos:
            user_pos.append(str(a) + " " + str(b))
    write_data = {
        "Number of Ground users": number_users,
        "Position of Ground users": user_pos
    }
    x = [float(point.split(' ')[0]) for point in user_pos]
    y = [float(point.split(' ')[1]) for point in user_pos]
    plt.scatter(x, y, label=f'Ground user')
    plt.legend()
    plt.title(f'Ground user location', fontweight="bold")
    plt.xlabel(f'X axis', fontweight='bold')
    plt.ylabel(f'Y axis', fontweight='bold')
    parent_dir = os.getcwd()
    file_name = "user_input.json"
    file_path = os.path.join(parent_dir, 'input_files', file_name)
    with open(file_path, 'w') as file_pointer:
        json.dump(write_data, file_pointer)
    file_name = "scenario_input.json"
    file_path = os.path.join(parent_dir, 'input_files', file_name)
    with open(file_path, 'r') as file_pointer:
        file_data = json.load(file_pointer)
    file_data["N"] = N
    file_data["M"] = M
    with open(file_path, 'w') as file_pointer:
        json.dump(file_data, file_pointer)
    file_name = "user_loc.png"
    file_path = os.path.join(parent_dir, 'input_files', file_name)
    plt.savefig(file_path)

if __name__ == "__main__":
    parent_dir = os.getcwd()
    file_name = 'user_location.json'
    file_path = os.path.join(parent_dir, 'input_files', file_name)
    with open(file_path, 'r') as file_pointer:
        file_data = json.load(file_pointer)
        N = file_data['N']
        M = file_data['M']
        number_users = file_data['Number of User']
    generate_user_input(N, M, number_users)

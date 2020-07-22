import os.path
import random
import json
import os


def generate_user_input(N, M, number_users):
    """
    Function: generate_user_input\n
    Parameter: (N, M) -> size of the grid, number_users -> Number of ground user needed to be placed\n
    Returns: nothing\n
    Functionality: Writes the output to file_name_passed and saves it in input_files\n
    """
    user_pos = []
    while len(user_pos) < number_users:
        a = random.randint(0, N - 1)
        b = random.randint(0, M - 1)
        if str(a) + " " + str(b) not in user_pos:
            user_pos.append(str(a) + " " + str(b))
    write_data = {
        "Number of Ground users": number_users,
        "Position of Ground users": user_pos
    }
    parent_dir = os.getcwd()
    file_name = str(N) + "_" + str(M) + "_" + str(number_users) + "_user.json"
    file_path = os.path.join(parent_dir, 'input_files', 'user_input_scenarios', file_name)
    with open(file_path, 'w') as file_pointer:
        json.dump(write_data, file_pointer)


if __name__ == "__main__":
    N = int(input("Enter the number of Rows in the grid: "))
    M = int(input("Enter the number of Columns in the grid: "))
    number_users = int(input("Enter the number of ground users: "))
    generate_user_input(N, M, number_users)

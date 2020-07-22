import random
import time
import json
import os


# (N, N) -> Size of the grid
N = 0
# rad -> communication radius of the UAV
rad = 0
# number_user -> Number of users in the grid
number_user = 0


def take_input():
    """
    Function: take_input\n
    Parameter: None\n
    Functionality: Takes the desired input and initializes the global variables\n
    """
    global N
    global rad
    global number_user
    N = int(input("Enter the size of the grid: "))
    rad = int(input("Enter the Communication radius of the UAV: ")) - 1
    number_user = int(input("Enter the number of users in the grid: "))


def generate_divisions():
    """
    Function: generate_divisions\n
    Parameter: None\n
    Returns: a list of the points the grid needs to be divided\n
    """
    division_lst = []
    num = 0
    while num <= N:
        division_lst.append(num)
        num += rad
    if division_lst[-1] < N:
        division_lst.append(N)
    return division_lst


def generate_subgrids():
    """
    Function: generate_subgrids\n
    Parameter: None\n
    Returns: list of subgrid points\n
    NOTE: Can be optimed in space and time complexity
    """
    i = 1
    j = 1
    division_lst = generate_divisions()
    sub_grid = []
    while (i < len(division_lst)):
        row_lst = []
        row_lst.append((division_lst[i], division_lst[j]))
        j += 1
        while (j < len(division_lst)):
            row_lst.append((division_lst[i], division_lst[j]))
            j += 1
        sub_grid.append(row_lst)
        j = 1
        i += 1
    return sub_grid


def distribute_users():
    """
    Function: distribute_users\n
    Parameters: None\n
    Returns: list of number of users in each subgrid
    """
    global number_user
    output_user_number = number_user
    sub_grids = generate_subgrids()
    division_lst = generate_divisions()
    N = len(sub_grids)
    M = len(sub_grids[0])
    number_grid = N * M
    if number_user % number_grid != 0:
        number_user += (number_grid - number_user % number_grid)
    number_user_subgrid = number_user // number_grid
    user_points = []
    is_non_uniform = False
    number_placed = 0
    number_square = 0
    for i in range(N):
        sub_grid_points = []
        for j in range(M):
            row, col = sub_grids[i][j]
            row %= rad
            col %= rad
            if row == 0:
                row = rad
            if col == 0:
                col = rad
            if row * col <= number_user_subgrid:
                sub_grid_points.append(row * col)
                number_placed += row * col
                is_non_uniform = True
            else:
                sub_grid_points.append(0)
                number_square += 1
        user_points.append(sub_grid_points)
    if is_non_uniform and number_square != 0:
        points_remaining = number_user - number_placed
        if points_remaining % number_square != 0:
            points_remaining += (number_square -
                                 points_remaining % number_square)
        user_in_grid = points_remaining // number_square
        for i in range(len(user_points)):
            for j in range((len(user_points[0]))):
                if user_points[i][j] == 0:
                    user_points[i][j] = user_in_grid
                    if user_in_grid > rad * rad:
                        user_points[i][j] = rad * rad
    else:
        for i in range(len(user_points)):
            for j in range((len(user_points[0]))):
                user_points[i][j] = number_user_subgrid
    return user_points


def generate_random_points():
    """
    Function: generate_random_points\n
    Parameter: None\n
    Returns: list of desired points\n
    """
    global number_user
    output_user_number = number_user
    sub_grids = generate_subgrids()
    division_lst = generate_divisions()
    N = len(sub_grids)
    M = len(sub_grids[0])
    number_grid = N * M
    if number_user % number_grid != 0:
        number_user += (number_grid - number_user % number_grid)
    number_user_subgrid = number_user // number_grid
    user_points = distribute_users()
    user_pos = []
    for i in range(N):
        sub_grid_user = []
        for j in range(M):
            print(f"Generating Points for sub-grid{i, j}")
            time.sleep(0.2)
            if len(user_pos) > output_user_number:
                break
            row, col = sub_grids[i][j]
            row %= rad
            col %= rad
            if row == 0:
                row = rad
            if col == 0:
                col = rad
            while len(sub_grid_user) < user_points[i][j]:
                x = random.randint(0, row - 1)
                y = random.randint(0, col - 1)
                x += division_lst[i]
                y += division_lst[j]
                if str(x) + " " + str(y) not in sub_grid_user:
                    sub_grid_user.append(str(x) + " " + str(y))
            user_pos += sub_grid_user
            sub_grid_user = []
    user_pos = sorted(user_pos[:output_user_number])
    return user_pos

def write_file ():
    """
    Function: write_file\n
    Parameters: None\n
    Functionality: Write the file to the location specified\n
    """
    global N
    user_pos = generate_random_points()
    write_data = {
        "Number of Ground users": len(user_pos),
        "Position of Ground users": user_pos
    }
    print(write_data)
    parent_dir = os.getcwd()
    file_name = str(N) + "_" + str(N) + "_" + str(len(user_pos)) + "_user.json"
    file_path = os.path.join(parent_dir, 'input_files',
                             'user_input_scenarios', file_name)
    with open(file_path, 'w') as file_pointer:
        json.dump(write_data, file_pointer)


if __name__ == "__main__":
    take_input()
    write_file()

import os
import os.path
import matplotlib.pyplot as plt


def get_points():
    """
    Function: get_points\n
    Parameters: None\n
    Returns: list of tuples containing coordinate points\n
    """
    parent_dir = os.getcwd()
    dir_name = 'analysis_output_files'
    file_name = 'scenario_analysis.log'
    file_path = os.path.join(parent_dir, dir_name, file_name)
    x = []
    y = []
    data = []
    with open(file_path, 'r') as file_pointer:
        data = file_pointer.readlines()
    for point in data[3:-3]:
        a = float(point.split(' ')[0])
        b = float(point.split(' ')[1])
        x.append(a)
        y.append(b)
    return (x, y)


if __name__ == "__main__":
    parent_dir = os.getcwd()
    dir_path = os.path.join(parent_dir, 'analysis_output_files')
    try:
        os.mkdir(dir_path)
    except OSError as error:
        pass
    y, x = get_points()
    plt.scatter(x,y)
    plt.title('UAV Communication Threshold vs Standard Deviation of User Distance')
    plt.xlabel('Standard Deviation of User Distance')
    plt.ylabel('UAV Communication Threshold')
    file_path = os.path.join (dir_path, 'scenario_analysis.png')
    plt.savefig(file_path)
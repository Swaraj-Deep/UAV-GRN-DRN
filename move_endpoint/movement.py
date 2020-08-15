import random
import math


def get_random_location(N, M):
    """
    Function: get_random_location\n
    Parameters: N -> Number of rows in the Grid, M -> Number of columns in the Grid\n
    Returns: a tuple of any random location which is inside the Grid\n
    """
    x = random.randint(0, N - 1)
    y = random.randint(0, M - 1)
    return (x, y)


def get_center_location(N, M):
    """
    Function: get_center_location\n
    Parameters: N -> Number of rows in the Grid, M -> Number of columns in the Grid\n
    Returns: a tuple of center location of the disaster area\n
    """
    x = N // 2
    y = M // 2
    return (x, y)


def get_centroid_location(N, M, UAV_location, UAV_to_UAV_threshold):
    """
    Function: get_center_location\n
    Parameters: N -> Number of rows in the Grid, M -> Number of columns in the Grid, UAV_location -> Dict of UAV locations, UAV_to_UAV_threshold -> threshold of the UAVs\n
    Returns: a tuple of centroid location of the placed UAV locations so far disaster area\n
    """
    size = len(UAV_location)
    x, y = (0, 0)
    if size < 2:
        return get_vicinity_location(N, M, UAV_location, UAV_to_UAV_threshold)
    else:
        for UAV, location in UAV_location.items():
            x_1, y_1 = location
            x += x_1
            y += y_1
        x //= size
        y //= size
        return (x, y)


def get_cell_vicinity(i, j, UAV_to_UAV_threshold, N, M):
    """
    Function: get_cell_vicinity\n
    Parameters\n
    i -> ith row of the grid\n
    j -> jth row of the grid\n
    UAV_to_UAV_threshold -> threshold of the UAV\n
    N -> number of rows in the grid\n
    M -> number of columns in the grid\n
    Returns: List of cells which can be reached from a particular location\n
    """
    up = max(0, i - UAV_to_UAV_threshold)
    left = max(0, j - UAV_to_UAV_threshold)
    down = min(N - 1, i + UAV_to_UAV_threshold)
    right = min(M - 1, j + UAV_to_UAV_threshold)
    cell_list = []
    for i in range(up, down + 1):
        cell_list.append((i, up))
    for i in range(up, down + 1):
        cell_list.append((up, i))
    for i in range(left, right + 1):
        cell_list.append((i, right))
    for i in range(left, right + 1):
        cell_list.append((right, i))
    # for i in range(up, down + 1):
    #     for j in range(left, right + 1):
    #         # cell_list.append ((i, j))
    return cell_list


def get_vicinity_location(N, M, UAV_location, UAV_to_UAV_threshold):
    """
    Function: get_vicinity_location\n
    Parameters: N -> Number of rows in the Grid, M -> Number of columns in the Grid\n
    Returns: a tuple of visinity location (within the range of UAV to UAV threshold) of one of the placed UAV so far disaster area\n
    """
    size = len(UAV_location)
    rand_UAV = random.randint(1, size)
    i, j = UAV_location[rand_UAV]
    cell_list = get_cell_vicinity(i, j, UAV_to_UAV_threshold, N, M)
    rand_loc = random.randint(0, len(cell_list) - 1)
    x, y = cell_list[rand_loc]
    return (x, y)


def get_random_move(loc, N, M):
    """
    Function: get_random_move\n
    Parameter: loc -> location of UAV on the Grid, N -> Rows in the Grid, M -> Columns in the Grid\n
    Returns: A tuple of valid random location where the UAV will be placed and the action taken\n
    """
    # 0 -> up
    # 1 -> right
    # 2 -> down
    # 3 -> left
    # 4 -> static
    dx = [-1, 0, 1, 0, 0]
    dy = [0, 1, 0, -1, 0]
    x, y = loc
    action = 0
    # In the last row
    if x == N - 1:
        # In the first cell of the last row
        if y == 0:
            # Possible move are up and right or static
            action = random.randint(0, 2)
            if action == 2:
                action = 4
        # In the last cell of the last row
        elif y == M - 1:
            # Possible moves are up and left or static
            action = random.randint(0, 2)
            # if move is right change to left
            if action == 1:
                action = 3
            if action == 2:
                action = 4
        # any where in the row except the above two cases
        else:
            # Possible moves are up, left, right
            action = random.randint(0, 3)
            if action == 3:
                action = 4
            # if move is down change to left
            if action == 2:
                action = 3
    # In the first row
    elif x == 0:
        # In the first cell of the first row
        if y == 0:
            # Possible moves are right and down or static
            action = random.randint(1, 3)
            if action == 3:
                action = 4
        # In the last cell of the first row
        elif y == M - 1:
            # Possible moves are left and down or static
            action = random.randint(2, 4)
        # any where in the row except the above two cases
        else:
            # Possible moves are left, right, down, static
            action = random.randint(1, 4)
    # In the last column
    elif y == M - 1:
        # In the first cell of the last column
        if x == 0:
            # Possible moves are left and down or static
            action = random.randint(2, 4)
        # In the last cell of the last column
        elif x == N - 1:
            # Possible moves are up and left or static
            action = random.randint(0, 2)
            if action == 2:
                action = 4
            # if the action is right change to left
            if action == 1:
                action = 3
        # any where in the column except the above two cases
        else:
            # Possible moves are up, left and down or static
            action = random.randint(0, 3)
            if action == 3:
                action = 4
            # if the action is right change to left
            if action == 1:
                action = 3
    # In the first column
    elif y == 0:
        # In the first cell of the first column
        if x == 0:
            # Possible moves are right and down or static
            action = random.randint(1, 3)
            if action == 3:
                action = 4
        # In the last cell of the first column
        elif x == N - 1:
            # Possible moves are right and up or static
            action = random.randint(0, 2)
            if action == 2:
                action = 4
        # any where in the column except the above two cases
        else:
            # Possible moves are up, right, down or static
            action = random.randint(0, 3)
            if action == 3:
                action = 4
    # In any other cell so can move in any direction
    else:
        action = random.randint(0, 4)
    x += dx[action]
    y += dy[action]
    power_factor = random.randint(0, 2)
    return (x, y, action, power_factor)


def get_euc_dist(pos_1, pos_2):
    """
    Function: get_euc_dist\n
    Parameters: pos_1 -> position of the first UAV, pos_2 -> position of the second UAV\n
    Returns: The euclidean distance between the two positions\n
    """
    x1, y1 = pos_1
    x2, y2 = pos_2
    dist = (x1 - x2) ** 2 + (y1 - y2) ** 2
    return math.sqrt(dist)


def map_2d_to_1d(loc, N):
    """
    Function: map_2d_to_1d\n
    Parameter: loc -> cell location which needs to be mapped in the 1D index, N -> number of rows in the grid\n
    Return: the index of the mapped location\n
    """
    x, y = loc
    return (((N - 1) * x) + y)


def map_1d_to_2d(index, N, M):
    """
    Function: map_1d_to_2d\n
    Parameter: index -> index which needs to be mapped to the 2D coordinates, N -> number of rows in the grid, M -> number of columns in the grid\n
    Return: the location of the mapped index\n
    """
    x = index // (N - 1)
    y = index % M
    return (x, y)

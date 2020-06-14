import random
import math


def get_random_location(N, M):
    """
    Function: get_random_location\n
    Parameters: N -> Number of rows in the Grid, M -> Number of columns in the Grid\n
    Returns: a tuple of any random location which is inside the Grid\n
    """
    # x = random.randint(((N - 1) // 2), N - 1)
    # y = random.randint(((M - 1) // 2), M - 1)
    x = random.randint (0, N - 1)
    y = random.randint (0, M - 1)
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
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]
    x, y = loc
    action = 0
    # In the last row
    if x == N - 1:
        # In the first cell of the last row
        if y == 0:
            # Possible move are up and right
            action = random.randint(0, 1)
        # In the last cell of the last row
        elif y == M - 1:
            # Possible moves are up and left
            action = random.randint(0, 1)
            # if move is right change to left
            if action == 1:
                action = 3
        # any where in the row except the above two cases
        else:
            # Possible moves are up, left, right
            action = random.randint(0, 2)
            # if move is down change to left
            if action == 2:
                action = 3
    # In the first row
    elif x == 0:
        # In the first cell of the first row
        if y == 0:
            # Possible moves are right and down
            action = random.randint(1, 2)
        # In the last cell of the first row
        elif y == M - 1:
            # Possible moves are left and down
            action = random.randint(2, 3)
        # any where in the row except the above two cases
        else:
            # Possible moves are left, right, down
            action = random.randint(1, 3)
    # In the last column
    elif y == M - 1:
        # In the first cell of the last column
        if x == 0:
            # Possible moves are left and down
            action = random.randint(2, 3)
        # In the last cell of the last column
        elif x == N - 1:
            # Possible moves are up and left
            action = random.randint(0, 1)
            # if the action is right change to left
            if action == 1:
                action = 3
        # any where in the column except the above two cases
        else:
            # Possible moves are up, left and down
            action = random.randint(0, 2)
            # if the action is right change to left
            if action == 1:
                action = 3
    # In the first column
    elif y == 0:
        # In the first cell of the first column
        if x == 0:
            # Possible moves are right and down
            action = random.randint(1, 2)
        # In the last cell of the first column
        elif x == N - 1:
            # Possible moves are right and up
            action = random.randint(0, 1)
        # any where in the column except the above two cases
        else:
            # Possible moves are up, right, down
            action = random.randint(0, 2)
    # In any other cell so can move in any direction
    else:
        action = random.randint(0, 3)
    x += dx[action]
    y += dy[action]
    return (x, y, action)


def get_dist_UAV(pos_1, pos_2):
    """
    Function: get_dist_UAV\n
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

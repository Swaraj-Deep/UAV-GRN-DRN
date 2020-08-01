import users_endpoint.users
import move_endpoint.movement
import grn_endpoint.grn_info


def reward_function(UAV_node, placed, pos_i, UAV_location, t, power_UAV, UAV_to_UAV_threshold, radius_UAV, N, M, ground_placed):
    """
    Function: reward_function\n
    Parameters: UAV_node -> the UAV which needs to be placed, placed -> list of already placed UAVs, pos_i -> current position of the UAV_node, UAV_location -> Dictionary storing locations of UAVs, t -> threshold distance of UAV, power_UAV -> power of UAV, UAV_to_UAV_threshold -> UAV to UAV communication threshold, radius_UAV -> radius of the UAV, (N, M) -> size of the grid, ground_placed -> list of users already placed\n
    Returns: the reward for this configuration\n
    """
    pos_reward = 1
    rho_reward = 0
    neg_reward = 1
    reward = 1
    pi = grn_endpoint.grn_info.get_PI()
    UAV_to_UAV_threshold += power_UAV // UAV_to_UAV_threshold
    radius_UAV += power_UAV // radius_UAV
    ground_users = users_endpoint.users.get_number_ground_users()
    # RHO function
    for j in placed:
        pos_j = UAV_location[j]
        if move_endpoint.movement.get_dist_UAV(pos_i, pos_j) < UAV_to_UAV_threshold:
            rho_reward = 1
            break
    # Outer Summation
    for j in placed:
        pos_j = UAV_location[j]
        emc_reward = 0
        if grn_endpoint.grn_info.is_edge_grn(grn_endpoint.grn_info.m(UAV_node), grn_endpoint.grn_info.m(j)):
            emc_reward = (grn_endpoint.grn_info.get_emc(
                grn_endpoint.grn_info.m(UAV_node), grn_endpoint.grn_info.m(j)) + 1) / (pi + 1)
        g_placed_i = set(
            users_endpoint.users.get_users_cell_connections(pos_i))
        ground_placed = set(ground_placed)
        user_conn = len(g_placed_i - ground_placed)
        user_den = ground_users
        user_conn /= user_den
        pos_reward = emc_reward + user_conn
        if move_endpoint.movement.get_dist_UAV(pos_i, pos_j) < UAV_to_UAV_threshold - t:
            neg_reward += 1
        reward += pos_reward / neg_reward
    reward *= rho_reward / power_UAV
    return reward


def user_coverage_count_xi_old(user, placed, UAV_location, radius_UAV, N, M):
    """
    Function: user_coverage_count_xi_old\n
    Parameters: user-> user to be checked, placed -> list of UAVs already placed, UAV_location -> dict containing position of placed UAVs, radius_UAV -> radius of UAV, (N, M) -> size of the grid\n
    Returns: Calculated reward
    """
    user_conn = 0
    for j in placed:
        pos_j = UAV_location[j]
        if users_endpoint.users.is_user_connected(user, pos_j, radius_UAV, N, M):
            user_conn += 1
    if user_conn == 0:
        user_conn = 1
    else:
        user_conn = 0
    return user_conn


def reward_function_old(UAV_node, placed, pos_i, UAV_location, t, power_UAV, UAV_to_UAV_threshold, radius_UAV, N, M):
    """
    Function: reward_function_old\n
    Parameters: UAV_node -> the UAV which needs to be placed, placed -> list of already placed UAVs, pos_i -> current position of the UAV_node, UAV_location -> Dictionary storing locations of UAVs, t -> threshold distance of UAV, power_UAV -> power of UAV, UAV_to_UAV_threshold -> UAV to UAV communication threshold, radius_UAV -> radius of the UAV, (N, M) -> size of the grid\n
    Returns: the reward for this configuration\n
    """
    pos_reward = 1
    rho_reward = 0
    neg_reward = 1
    reward = 1
    pi = grn_endpoint.grn_info.get_PI()
    ground_users = users_endpoint.users.get_number_ground_users()
    # RHO function
    for j in placed:
        pos_j = UAV_location[j]
        if move_endpoint.movement.get_dist_UAV(pos_i, pos_j) < UAV_to_UAV_threshold:
            rho_reward = 1
            break
    # Outer Summation
    for j in placed:
        pos_j = UAV_location[j]
        emc_reward = 0
        if grn_endpoint.grn_info.is_edge_grn(grn_endpoint.grn_info.m(UAV_node), grn_endpoint.grn_info.m(j)):
            emc_reward = (grn_endpoint.grn_info.get_emc(
                grn_endpoint.grn_info.m(UAV_node), grn_endpoint.grn_info.m(j)) + 1) / (pi + 1)
        user_conn = 0
        for k in range(1, ground_users + 1):
            user_conn = 0
            if users_endpoint.users.is_user_connected(k, pos_i, radius_UAV, N, M):
                user_conn = 1
            user_conn *= user_coverage_count_xi_old(
                k, placed, UAV_location, radius_UAV, N, M)
        user_den = ground_users * len(placed)
        user_conn /= user_den
        pos_reward = emc_reward + user_conn
        if move_endpoint.movement.get_dist_UAV(pos_i, pos_j) < t:
            neg_reward += 1
        reward += pos_reward / neg_reward
    reward *= rho_reward / power_UAV
    return reward

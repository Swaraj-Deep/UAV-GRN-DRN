import users_endpoint.users
import move_endpoint.movement
import grn_endpoint.grn_info


def is_equal(list_1, list_2):
    """
    Function: is_equal\n
    Parameters: list_1 -> first list, list_2 -> second list\n
    Return: True if both list_1 and list_2 are equal else False
    """
    if len(list_1) != len(list_2):
        return False
    len_list = 0
    for item in list_2:
        if item in list_1:
            len_list += 1
    if len_list == len(list_1):
        return True
    return False


def reward_function(UAV_node, placed, pos_i, UAV_location, t, power_UAV, UAV_to_UAV_threshold):
    """
    Function: reward_function\n
    Parameters: UAV_node -> the UAV which needs to be placed, placed -> list of already placed UAVs, pos_i -> current position of the UAV_node, UAV_location -> Dictionary storing locations of UAVs, t -> threshold distance of UAV, power_UAV -> power of UAV, UAV_to_UAV_threshold -> UAV to UAV communication threshold\n
    Returns: the reward for this configuration\n
    """
    neg_reward = 1
    pos_reward = 1
    ground_users = users_endpoint.users.get_number_ground_users()
    user_served_temp = set()
    connectivity = users_endpoint.users.get_ground_cell_connections(pos_i)
    if connectivity == 0:
        neg_reward += 9999999
    user_connected_i = users_endpoint.users.get_users_cell_connections(pos_i)
    for j in placed:
        pos_j = UAV_location[j]
        user_connected_j = users_endpoint.users.get_users_cell_connections(
            pos_j)
        for user in user_connected_j:
            user_served_temp.add(user)
        if is_equal(user_connected_i, user_connected_j):
            neg_reward += 999999
        else:
            pos_reward += 99999
    if len(user_served_temp) / ground_users < 1:
        neg_reward += 999999
    for j in placed:
        pos_j = UAV_location[j]
        dist_uav = move_endpoint.movement.get_dist_UAV(pos_i, pos_j)
        if dist_uav == 0 or dist_uav <= t:
            neg_reward += 99999999 * -999
        # if dist_uav > t and dist_uav <= UAV_to_UAV_threshold:
        #     if grn_endpoint.grn_info.is_edge_grn(UAV_node, j) or grn_endpoint.grn_info.is_edge_grn(j, UAV_node):
        #         pos_reward += 99999
        #     else:
        #         pos_reward += 9999
    # New additions
    for j in placed:
        pos_j = UAV_location[j]
        if grn_endpoint.grn_info.is_edge_grn(UAV_node, j) or grn_endpoint.grn_info.is_edge_grn(j, UAV_node):
            if move_endpoint.movement.get_dist_UAV(pos_i, pos_j) < UAV_to_UAV_threshold:
                pos_reward += 9999
            pos_reward += grn_endpoint.grn_info.get_emc(grn_endpoint.grn_info.m(UAV_node), grn_endpoint.grn_info.m(j)) + 9999
            pos_reward += grn_endpoint.grn_info.get_emc(grn_endpoint.grn_info.m(j), grn_endpoint.grn_info.m(UAV_node)) + 9999
        else:
            neg_reward += 999999
    # New Additions over
    reward = pos_reward / neg_reward
    reward *= power_UAV
    return reward


def reward_function_paper(UAV_node, placed, pos_i, UAV_location, t, power_UAV, UAV_to_UAV_threshold):
    """
    Function: reward_function\n
    Parameters: UAV_node -> the UAV which needs to be placed, placed -> list of already placed UAVs, pos_i -> current position of the UAV_node, UAV_location -> Dictionary storing locations of UAVs, t -> threshold distance of UAV, power_UAV -> power of UAV, UAV_to_UAV_threshold -> UAV to UAV communication threshold\n
    Returns: the reward for this configuration\n
    """
    pos_reward = 0
    rho_reward = 0
    neg_reward = 1
    # RHO function
    for j in placed:
        pos_j = UAV_location[j]
        if move_endpoint.movement.get_dist_UAV(pos_i, pos_j) < UAV_to_UAV_threshold:
            rho_reward = 1
            break
    # Indicator variable edge motif centrality
    for j in placed:
        if grn_endpoint.grn_info.is_edge_grn(UAV_node, j):
            pos_reward += grn_endpoint.grn_info.get_emc(grn_endpoint.grn_info.m(UAV_node), grn_endpoint.grn_info.m(j)) + 1
    # ETA function
    eta_num = users_endpoint.users.get_ground_cell_connections(pos_i)
    eta_den = 1
    for j in placed:
        pos_j = UAV_location[j]
        eta_den += users_endpoint.users.get_ground_cell_connections(pos_j) + 1
    pos_reward += eta_num / eta_den
    # Indicator variable for denominator
    for j in placed:
        pos_j = UAV_location[j]
        if move_endpoint.movement.get_dist_UAV(pos_i, pos_j) < t:
            neg_reward += 1
    # Calculating reward
    reward = pos_reward / neg_reward
    reward *= power_UAV * rho_reward
    return reward

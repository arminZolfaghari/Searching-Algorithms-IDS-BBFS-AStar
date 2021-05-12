from collections import defaultdict
from AdditionalFunctions import *
from Node import *
import time


def create_child(node):
    children_arr = []
    curr_environment, curr_robot_coordinates, curr_depth = node.environment, node.robot_coordinates, node.depth
    all_permitted_movements = get_all_permitted_movements(curr_environment, curr_robot_coordinates)
    for movement in all_permitted_movements:
        new_environment, new_robot_coordinates = update_environment(curr_environment, curr_robot_coordinates, movement)
        child_node = Node(new_environment, new_robot_coordinates, curr_depth + 1, movement, node, node.cost_g + 1, 0)
        children_arr.insert(0, child_node)

    return children_arr


# depth limited search
def dls(start_node, all_goal_environment, max_depth, nodes_info):
    nodes_info[1] += 1  # num_of_expand
    if start_node.environment in all_goal_environment:
        return start_node
    if max_depth <= 0:
        return False

    children = create_child(start_node)
    nodes_info[0] += len(children)  # num_of_generate

    for child in children:
        goal_node = dls(child, all_goal_environment, max_depth - 1, nodes_info)
        if goal_node:
            return goal_node
    return False


# It uses recursive dls()
def ids(first_node, all_goal_environment, max_depth):
    nodes_info = [0, 0]  # nodes_info[0] is num_of_generates , nodes_info[1] is num_of_expanded
    for depth in range(max_depth):
        goal_node = dls(first_node, all_goal_environment, depth, nodes_info)

        if goal_node:
            return True, goal_node, nodes_info
    return False, "", nodes_info


def start_ids_algorithm(test_case_file, max_depth):
    environment = read_file(test_case_file)[1]
    robot_coordinates = read_file(test_case_file)[4]
    all_goal_environment = generate_all_goal_environment(test_case_file)[0]
    root_node = Node(environment, robot_coordinates, 0, "", "", 1, 0)

    result_of_IDS, received_final_state, nodes_info = ids(root_node, all_goal_environment, max_depth)

    if result_of_IDS:
        path = find_path_with_final_node(received_final_state)
        return result_of_IDS, path, received_final_state.depth, nodes_info
    else:
        return result_of_IDS, received_final_state, max_depth, nodes_info

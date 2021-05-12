from AdditionalFunctions import *
from Node import *
import time
import copy


def calculate_manhattan_distance(point1, point2):
    x_point1, y_point1 = point1['x'], point1['y']
    x_point2, y_point2 = point2['x'], point2['y']

    return abs(x_point1 - x_point2) + abs(y_point1 - y_point2)


def find_butter_for_plate(butters_coordinates_arr, plates_coordinates_arr):
    butters_arr_sorted = []
    plates_arr_sorted = []
    for butter_coordinates in butters_coordinates_arr:
        res_plate = plates_coordinates_arr[0]
        min_distance = calculate_manhattan_distance(butter_coordinates, res_plate)
        for plate_coordinates in plates_coordinates_arr:
            distance = calculate_manhattan_distance(butter_coordinates, plate_coordinates)
            if min_distance > distance:
                res_plate = plate_coordinates

        butters_arr_sorted.append(butter_coordinates)
        plates_arr_sorted.append(res_plate)
        plates_coordinates_arr.remove(res_plate)

    return butters_arr_sorted, plates_arr_sorted


def find_closest_plate(now_coordinates, plates_coordinates):
    distance_arr = []
    for plate_coordinates in plates_coordinates:
        distance_arr.append(calculate_manhattan_distance(now_coordinates, plate_coordinates))

    best_plate_index = distance_arr.index(min(distance_arr))
    best_plate = plates_coordinates[best_plate_index]
    return best_plate


def calculate_distance_point_to_all_plates(point, plates_coordinates_arr):
    distance = 0
    point_copy = point
    plates_coordinates_arr_copy = copy.deepcopy(plates_coordinates_arr)
    while plates_coordinates_arr_copy:
        best_plate = find_closest_plate(point_copy, plates_coordinates_arr_copy)
        plates_coordinates_arr_copy.remove(best_plate)
        distance += calculate_manhattan_distance(point_copy, best_plate)
        # print(point_copy)
        # print(best_plate)
        # print(distance)
        point_copy = best_plate
    # print("***************")

    return distance


def calculate_heuristic_environment(plates_coordinates_arr, environment_without_cost):
    num_rows, num_cols = len(environment_without_cost), len(environment_without_cost[0])
    heuristic_environment = [[0 for i in range(num_cols)] for j in range(num_rows)]

    for i in range(num_rows):
        for j in range(num_cols):
            heuristic_environment[i][j] = calculate_distance_point_to_all_plates({"x": i, "y": j},
                                                                                 plates_coordinates_arr)

    return heuristic_environment


def get_heuristic_point(point):
    return


# sort frontier list by cost nodes
def sort_frontier_by_cost(frontier):
    frontier.sort(key=lambda x: x.cost_f, reverse=False)


# return cost of point
def calculate_cost_f_node(new_cost_g, new_robot_coordinates, huerisitic_arr):
    return int(new_cost_g) + huerisitic_arr[new_robot_coordinates['x']][new_robot_coordinates['y']]


def calculate_cost_g_node(environment_cost, new_robot_coordinates, curr_cost_g):
    return int(curr_cost_g) + int(environment_cost[new_robot_coordinates['x']][new_robot_coordinates['y']])


def is_new_node_in_frontier(frontier, new_node):
    for node in frontier:
        if node.environment == new_node.environment:
            return True, node
    return False, new_node


def is_new_node_in_explored(explored, new_node):
    for node in explored:
        if node.environment == new_node.environment:
            return True
    return False


def update_frontier_explored(frontier, explored, new_node):
    if not is_new_node_in_explored(explored, new_node):
        is_duplicate, duplicate_node = is_new_node_in_frontier(frontier, new_node)
        if is_duplicate:
            if new_node.cost_f < duplicate_node.cost_f:
                frontier.remove(duplicate_node)
                frontier.append(new_node)
        else:
            frontier.append(new_node)

    sort_frontier_by_cost(frontier)


def generate_node(node, envrironment_cost, hueristic_arr, frontier, explored):
    curr_environment, curr_robot_coordinates, curr_depth = node.environment, node.robot_coordinates, node.depth
    curr_cost_g, curr_cost_f = node.cost_g, node.cost_f
    all_permitted_movements = get_all_permitted_movements(curr_environment, curr_robot_coordinates)
    for movement in all_permitted_movements:
        new_environment, new_robot_coordinates = update_environment(curr_environment, curr_robot_coordinates, movement)
        new_cost_g = calculate_cost_g_node(envrironment_cost, new_robot_coordinates, curr_cost_g)
        new_cost_f = calculate_cost_f_node(new_cost_g, new_robot_coordinates, hueristic_arr)
        new_node = Node(new_environment, new_robot_coordinates, curr_depth + 1, movement, node, new_cost_g, new_cost_f)
        update_frontier_explored(frontier, explored, new_node)


def expanding_node(node, environment_cost, hueristic_arr, frontier, explored):
    generate_node(node, environment_cost, hueristic_arr, frontier, explored)
    explored.append(node)


def a_star_algorithm(start_node, max_depth, envrironment_cost, hueristic_arr, all_goal_environment):
    frontier, explored = [start_node], []
    expand_node = start_node
    is_receive, goal_state = False, 0
    while expand_node.depth <= max_depth:
        if expand_node.environment in all_goal_environment:
            is_receive, goal_state = True, expand_node
            break
        expanding_node(expand_node, envrironment_cost, hueristic_arr, frontier, explored)
        frontier.remove(expand_node)

        if len(frontier) == 0:
            break
        expand_node = frontier[0]

    if is_receive:
        return True, goal_state
    else:
        return False, "can't pass the butter"


# get final node(goal state) and return path from start node to goal node
def find_path_with_final_node(node):
    path_by_nodes = []
    pre_node = node

    while pre_node != "":
        path_by_nodes.append(pre_node)
        pre_node = pre_node.parent

    path_by_nodes.reverse()
    return path_by_nodes


def start_a_star_algorithm(test_case_file, max_depth):
    environment_without_cost = read_file(test_case_file)[1]
    environment_cost = read_file(test_case_file)[2]
    robot_coordinates = read_file(test_case_file)[4]
    all_goal_environment = generate_all_goal_environment(test_case_file)[0]
    arr_plates = find_plates_coordinates(test_case_file)
    heuristic = calculate_heuristic_environment(arr_plates, environment_without_cost)
    root_cost_g = environment_cost[robot_coordinates['x']][robot_coordinates['y']]
    root_cost_f = heuristic[robot_coordinates['x']][robot_coordinates['y']]
    root_node = Node(environment_without_cost, robot_coordinates, 0, "", "", root_cost_g, root_cost_f)

    result_of_a_star_algorithm, received_final_state = a_star_algorithm(root_node, max_depth, environment_cost,
                                                                        heuristic, all_goal_environment)
    if result_of_a_star_algorithm:
        path = find_path_with_final_node(received_final_state)
        return result_of_a_star_algorithm, path, received_final_state.depth
    else:
        return result_of_a_star_algorithm, received_final_state, max_depth

from collections import defaultdict
from AdditionalFunctions import *
from Node import *
import time


# def create_child(node, frontier):
#     curr_environment, curr_robot_coordinates, curr_depth = node.environment, node.robot_coordinates, node.depth
#     all_permitted_movements = get_all_permitted_movements(curr_environment, curr_robot_coordinates)
#     for movement in all_permitted_movements:
#         new_environment, new_robot_coordinates = update_environment(curr_environment, curr_robot_coordinates, movement)
#         child_node = Node(new_environment, new_robot_coordinates, curr_depth + 1, movement, node)
#         frontier.insert(0, child_node)
#
#     return frontier

def create_child(node):
    children_arr = []
    curr_environment, curr_robot_coordinates, curr_depth = node.environment, node.robot_coordinates, node.depth
    all_permitted_movements = get_all_permitted_movements(curr_environment, curr_robot_coordinates)
    for movement in all_permitted_movements:
        new_environment, new_robot_coordinates = update_environment(curr_environment, curr_robot_coordinates, movement)
        child_node = Node(new_environment, new_robot_coordinates, curr_depth + 1, movement, node, 0, 0)
        children_arr.insert(0, child_node)

    return children_arr


# depth limited search
nodes = []


def dls(start_node, all_goal_environment, max_depth):
    if start_node.environment in all_goal_environment:
        return start_node
    if max_depth <= 0:
        return False

    children = create_child(start_node)
    for child in children:
        goal_node = dls(child, all_goal_environment, max_depth - 1)
        if goal_node:
            return goal_node
    return False

    # def create_child(self, frontier):
    #     curr_environment, curr_robot_coordinates, curr_depth = self.environment, self.robot_coordinates, self.depth
    #     all_permitted_movements = get_all_permitted_movements(curr_environment, curr_robot_coordinates)
    #     print(curr_environment)
    #     for movement in all_permitted_movements:
    #         print("_______________________")
    #         print(curr_environment)
    #         new_environment, new_robot_coordinates = update_environment(self.environment, self.robot_coordinates,
    #                                                                     movement)
    #         print(new_environment)
    #         child_node = Node(new_environment, new_robot_coordinates, curr_depth + 1, movement)
    #         frontier.insert(0, child_node)
    #
    #     return frontier


# It uses recursive dls()
def ids(first_node, all_goal_environment, max_depth):
    for depth in range(max_depth):
        goal_node = dls(first_node, all_goal_environment, depth)
        if goal_node:
            return goal_node
    return False


def start_ids_algorithm(test_case_file, max_depth):
    environment = read_file(test_case_file)[1]
    robot_coordinates = read_file(test_case_file)[4]
    all_goal_environment = generate_all_goal_environment(test_case_file)[0]
    root_node = Node(environment, robot_coordinates, 0, "", "", 0, 0)
    start_time = time.time()
    path_to_goal_nodes = ids(root_node, all_goal_environment, max_depth)
    finish_time = time.time()
    duration = (finish_time - start_time)

    print(environment)
    if len(path_to_goal_nodes) > 0:
        print_path_with_nodes(path_to_goal_nodes[1:])
    else:
        print("can't pass the butter")

    print("depth : ", len(path_to_goal_nodes[1:]))
    print("duration(s) : ", duration)


def print_path_with_nodes(arr):
    for node in reversed(arr):
        print("*********************************************************")
        print(node.movement)
        print(node.environment)


if __name__ == "__main__":
    start_ids_algorithm("test1.txt", 15)

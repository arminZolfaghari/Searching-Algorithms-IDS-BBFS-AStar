from collections import defaultdict
from AdditionalFunctions import *
from Node import *


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
        child_node = Node(new_environment, new_robot_coordinates, curr_depth + 1, movement, node)
        children_arr.insert(0, child_node)

    return children_arr


# depth limited search
movements = []


def dls(start_node, all_goal_environment, max_depth):
    if start_node.environment in all_goal_environment:
        movements.append(start_node.movement)
        return movements
    if max_depth <= 0:
        return []

    children = create_child(start_node)
    for child in children:
        print(child.environment)
        movement = dls(child, all_goal_environment, max_depth - 1)
        if len(movement) > 0:
            movements.append(child.movement)
            return movements
        print("________________________________________________________________")
    return []

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


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    # for add edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # Depth Limited Search
    def DLS(self, src, target, max_depth):
        if src == target:
            return True
        if max_depth <= 0:
            return False
        # Recursive for all the vertices adjacent to this vertex
        for v in self.graph[src]:
            if self.DLS(v, target, max_depth - 1):
                return True
        return False

    # Recursive DLS (Iterative Deepening Search)
    def IDS(self, src, target, max_depth):
        for depth in range(max_depth):
            if self.DLS(src, target, depth):
                return True
        return False


def ids(first_node, all_goal_environment, max_depth):
    for depth in range(max_depth + 1):
        movements = dls(first_node, all_goal_environment, depth)
        if len(movements):
            return movements
    return []


if __name__ == "__main__":
    environment_with_cost, environment_without_cost, environment_cost, number_of_butters, robot_coordinates = read_file(
        "test3.txt")
    print(environment_without_cost)
    all_goal_environment, all_goal_robot_coordinates = generate_all_goal_environment("test3.txt")
    print(all_goal_environment)
    start_node = Node(environment_without_cost, robot_coordinates, 0, "", "")
    print(ids(start_node, all_goal_environment, 15))

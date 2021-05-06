from collections import defaultdict
from AdditionalFunctions import *


def create_child(node, frontier):
    curr_environment, curr_robot_coordinates, curr_depth = node.environment, node.robot_coordinates, node.depth
    all_permitted_movements = get_all_permitted_movements(curr_environment, curr_robot_coordinates)
    print(curr_environment)
    for movement in all_permitted_movements:
        print("_______________________")
        new_environment, new_robot_coordinates = update_environment(curr_environment, curr_robot_coordinates, movement)
        print(curr_environment)
        print(new_environment)
        child_node = Node(new_environment, new_robot_coordinates, curr_depth + 1, movement)
        frontier.insert(0, child_node)

    return frontier


class Node:
    def __init__(self, environment, robot_coordinates, depth, movement):
        self.environment = environment
        self.robot_coordinates = robot_coordinates
        self.depth = depth
        self.movement = movement

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


if __name__ == "__main__":
    environment_with_cost, environment_without_cost, environment_cost, number_of_butters, robot_coordinates = read_file(
        "test1.txt")
    print(environment_without_cost)
    start_node = Node(environment_without_cost, robot_coordinates, 0, " ")
    frontier = []
    new_frontier = create_child(start_node, frontier)
    # new_frontier = create_child(start_node, frontier)
    # for node in new_frontier:
    #     print(node.environment)


    # g = Graph(7)
    # g.addEdge(0, 1)
    # g.addEdge(0, 2)
    # g.addEdge(1, 3)
    # g.addEdge(1, 4)
    # g.addEdge(2, 5)
    # g.addEdge(2, 6)
    #
    # target = 6
    # maxDepth = 3
    # src = 0
    #
    # print(g.IDS(src, target, maxDepth))

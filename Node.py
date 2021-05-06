class Node:
    def __init__(self, environment, robot_coordinates, depth, movement):
        self.environment = environment
        self.robot_coordinates = robot_coordinates
        self.depth = depth
        self.movement = movement
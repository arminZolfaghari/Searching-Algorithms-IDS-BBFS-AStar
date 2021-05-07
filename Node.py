class Node:
    def __init__(self, environment, robot_coordinates, depth, movement, parent):
        self.environment = environment
        self.robot_coordinates = robot_coordinates
        self.depth = depth
        self.movement = movement
        self.parent = parent

class Initial_node:
    def __init__(self, environment):
        self.depth = -1
        self.environment = environment
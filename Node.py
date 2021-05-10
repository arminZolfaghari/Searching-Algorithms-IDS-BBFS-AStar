class Node:
    def __init__(self, environment, robot_coordinates, depth, movement, parent, cost_g, cost_f):
        self.environment = environment
        self.robot_coordinates = robot_coordinates
        self.depth = depth
        self.movement = movement
        self.parent = parent
        self.cost_g = cost_g
        self.cost_f = cost_f

    # def __eq__(self, others):
    #     if self.environment == others.environment


class Initial_node:
    def __init__(self, environment):
        self.depth = -1
        self.environment = environment

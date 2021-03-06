from AdditionalFunctions import *
from Node import Node, Initial_node
import copy
from AStar import is_new_node_in_explored, is_new_node_in_frontier

move_to_coordinate = {'u': {"x": -1}, 'r': {"y": +1}, 'd': {"x": +1}, 'l': {"y": -1}}


# this function checks whether we reach the end of the BBFS Algorithm or not.
# if two exact environments in forward frontier and backward frontier are found then it's finished.
def end_checker(forward_explored, backward_explored):
    for forward_node in forward_explored:
        for backward_node in backward_explored:
            if forward_node.environment == backward_node.environment:
                return forward_node, backward_node.parent
    return None


# creating children in BFS is not the same with IDS. in BFS children are added at the end of the frontier queue
def bfs(node, frontier, direction, nodes_info, explored):
    curr_environment, curr_robot_coordinates, curr_depth = node.environment, node.robot_coordinates, node.depth
    all_permitted_movements = get_all_permitted_movements(curr_environment, curr_robot_coordinates)
    nodes_info[0] += len(all_permitted_movements)

    all_children = []
    for movement in all_permitted_movements:
        if direction == 'forward':
            new_environment, new_robot_coordinates = update_environment(node.environment, node.robot_coordinates, movement)
            child_node = Node(new_environment, new_robot_coordinates, curr_depth + 1, movement, node, "", "")
            all_children.append(child_node)

        elif direction == 'backward':   # we may have more than one environment
            new_environments, new_robot_coordinates, only_one_child = update_environment_backward(node.environment, node.robot_coordinates, movement)

            first_child_node = Node(new_environments[0], new_robot_coordinates, curr_depth + 1, movement, node, "", "")
            all_children.append(first_child_node)
            if not only_one_child:
                second_child_node = Node(new_environments[1], new_robot_coordinates, curr_depth + 1, movement, node, "", "")
                all_children.append(second_child_node)


    # new states should be checked. they should not be repetetive states.
    for child in all_children:
        is_in_explored = is_new_node_in_explored(explored, child)
        is_in_frontier, _ = is_new_node_in_frontier(frontier, child)
        if not is_in_explored and not is_in_frontier:
            frontier.append(child)

    return frontier, nodes_info, explored


# this function return the cell in  environment if we move in the oposite direction of movement.
def reverse_movement(environment, robot_coordinates, movement, is_goal):
    num_rows, num_cols = len(environment), len(environment[0])

    if movement == 'u' and robot_coordinates['x'] + 1 < num_rows:
        if is_goal:
            environment[robot_coordinates['x'] + 1][robot_coordinates['y']] = 'p'
        return environment[robot_coordinates['x'] + 1][robot_coordinates['y']]

    elif movement == 'd' and robot_coordinates['x'] - 1 >= 0:
        if is_goal:
            environment[robot_coordinates['x'] - 1][robot_coordinates['y']] = 'p'
        return environment[robot_coordinates['x'] - 1][robot_coordinates['y']]

    elif movement == 'l' and robot_coordinates['y'] + 1 < num_cols:
        if is_goal:
            environment[robot_coordinates['x']][robot_coordinates['y'] + 1] = 'p'
        return environment[robot_coordinates['x']][robot_coordinates['y'] + 1]

    elif movement == 'r' and robot_coordinates['y'] - 1 >= 0:
        if is_goal:
            environment[robot_coordinates['x']][robot_coordinates['y'] - 1] = 'p'
        return environment[robot_coordinates['x']][robot_coordinates['y'] - 1]


# this function updates environment backward (from goal state to initial state).
def update_environment_backward(environment, current_robot_coordinates, movement):
    is_there_only_one_child = True
    new_robot_coordinates = dsum(current_robot_coordinates, move_to_coordinate[movement])
    curr_robot_x_coordinate, curr_robot_y_coordinate = current_robot_coordinates['x'], current_robot_coordinates['y']
    new_robot_x_coordinate, new_robot_y_coordinate = new_robot_coordinates['x'], new_robot_coordinates['y']

    new_environment = copy.deepcopy(environment)
    new_environment2 = copy.deepcopy(environment)

    returned_environments = [new_environment, new_environment2]

    # next robot coordinates have plate
    if returned_environments[0][new_robot_x_coordinate][new_robot_y_coordinate] == 'p':
        returned_environments[0][curr_robot_x_coordinate][curr_robot_y_coordinate] = ''
        returned_environments[0][new_robot_x_coordinate][new_robot_y_coordinate] = 'rp'

    elif returned_environments[0][new_robot_x_coordinate][new_robot_y_coordinate] == '' and \
            returned_environments[0][curr_robot_x_coordinate][curr_robot_y_coordinate] == 'rp':
        returned_environments[0][curr_robot_x_coordinate][curr_robot_y_coordinate] = 'p'
        returned_environments[0][new_robot_x_coordinate][new_robot_y_coordinate] = 'r'

    # set new coordinates for butter
    elif reverse_movement(returned_environments[0], current_robot_coordinates, movement, False) == 'b':
        is_there_only_one_child = False
        returned_environments[0][curr_robot_x_coordinate][curr_robot_y_coordinate] = 'b'
        returned_environments[0][new_robot_x_coordinate][new_robot_y_coordinate] = 'r'

        returned_environments[1][curr_robot_x_coordinate][curr_robot_y_coordinate] = ''
        returned_environments[1][new_robot_x_coordinate][new_robot_y_coordinate] = 'r'

    # if butter is on goal state
    elif reverse_movement(returned_environments[0], current_robot_coordinates, movement, False) == 'bp':
        reverse_movement(returned_environments[0], current_robot_coordinates, movement, True)
        is_there_only_one_child = False
        returned_environments[0][curr_robot_x_coordinate][curr_robot_y_coordinate] = 'b'
        returned_environments[0][new_robot_x_coordinate][new_robot_y_coordinate] = 'r'

        returned_environments[1][curr_robot_x_coordinate][curr_robot_y_coordinate] = ''
        returned_environments[1][new_robot_x_coordinate][new_robot_y_coordinate] = 'r'

    else:
        returned_environments[0][curr_robot_x_coordinate][curr_robot_y_coordinate] = ''
        returned_environments[0][new_robot_x_coordinate][new_robot_y_coordinate] = 'r'

    return returned_environments, new_robot_coordinates, is_there_only_one_child


def create_final_nodes(goal_environments, goal_robots_coordinates):
    backward_frontier = []
    initial_node = Initial_node([])
    for i in range(len(goal_environments)):  # or len(goal_robots_coordinates) it doesn't matter
        backward_frontier.append(Node(goal_environments[i], goal_robots_coordinates[i], 0, ' ', initial_node, "", ""))

    return backward_frontier


def find_move(src_node, dest_node):
    if src_node.robot_coordinates['x'] == dest_node.robot_coordinates['x'] and src_node.robot_coordinates['y'] < \
            dest_node.robot_coordinates['y']:
        return 'r'
    if src_node.robot_coordinates['x'] == dest_node.robot_coordinates['x'] and src_node.robot_coordinates['y'] > \
            dest_node.robot_coordinates['y']:
        return 'l'
    if src_node.robot_coordinates['x'] > dest_node.robot_coordinates['x'] and src_node.robot_coordinates['y'] == \
            dest_node.robot_coordinates['y']:
        return 'u'
    if src_node.robot_coordinates['x'] < dest_node.robot_coordinates['x'] and src_node.robot_coordinates['y'] == \
            dest_node.robot_coordinates['y']:
        return 'd'


def find_path(intersected_node, backward_node, goal_environments):
    path, path2 = [], []
    tmp_node = copy.deepcopy(intersected_node)
    tmp_node_back = copy.deepcopy(backward_node)

    while tmp_node.depth >= 0:
        path.insert(0, tmp_node)
        tmp_node = copy.deepcopy(tmp_node.parent)

    while tmp_node_back.depth >= 0:
        path2.append(tmp_node_back)
        if tmp_node_back.environment in goal_environments:
            tmp_node_back = copy.deepcopy(tmp_node_back.parent)
            break
        else:
            tmp_node_back = copy.deepcopy(tmp_node_back.parent)

    print_path(path)
    path2[0].movement = find_move(path[-1], path2[0])
    for p in range(1, len(path2)):
        path2[p].movement = find_move(path2[p - 1], path2[p])

    for p in path2:
        path.append(p)

    return path


def BBFS(file_name):
    # nodes_info = [num_created_nodes, num_expanded_nodes]
    nodes_info = [0, 0]
    forward_explored, backward_explored = [], []   # explored lists
    forward_frontier, backward_frontier = [], []   # frontier lists

    has_result = True
    environment_with_cost, environment_without_cost, environment_cost, number_of_butters, robot_coordinates = read_file(file_name)

    # initialize robot coordinates to initial node
    initial_node = Initial_node([])
    starting_node = Node(environment_without_cost, robot_coordinates, 0, ' ', initial_node, "", "")
    forward_frontier.insert(0, starting_node)
    nodes_info[0] += 1

    # this function returns all the possible goal states. but it's not enough. nodes are needed for backward bfs.
    goal_environments, goal_robots_coordinates = generate_all_goal_environment(file_name)
    backward_frontier = create_final_nodes(goal_environments, goal_robots_coordinates)
    nodes_info[0] += len(goal_environments)

    # create childern of initial node and then create childern in a loop until we reach Goal state
    while True:
        if len(forward_frontier) > 0:
            nodes_info[1] += 1
            forward_explored.append(forward_frontier.pop(0))
            forward_frontier, nodes_info, forward_explored = bfs(forward_explored[-1], forward_frontier, 'forward', nodes_info, forward_explored)

        # backward dfs should be called here
        if len(backward_frontier) > 0:
            nodes_info[1] += 1
            backward_explored.append(backward_frontier.pop(0))
            backward_frontier, nodes_info, backward_explored = bfs(backward_explored[-1], backward_frontier, 'backward', nodes_info, backward_explored)

        # environment with no solution should be handled
        result = end_checker(forward_explored, backward_explored)
        if result is not None:
            intersected_node, backward_node = result
            break

        if len(forward_frontier) == 0:
            path = ['no answer']
            has_result = False
            return has_result, path, nodes_info
        # check if we have answer at all!
        # if (forward_frontier[-1].depth + backward_frontier[-1].depth) > (len(environment_without_cost) * len(environment_without_cost[0])):
        #     path = ['no answer']
        #     has_result = False
        #     return has_result, path, nodes_info

    # find and print final path
    path = find_path(intersected_node, backward_node, goal_environments)
    return has_result, path, nodes_info
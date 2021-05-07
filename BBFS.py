from AdditionalFunctions import *
from Node import Node, Initial_node
import copy

def print_frontier(frontier):
    for f in frontier:
        print('r in frontier: ', f.robot_coordinates)


# this function checks whether we reach the end of the BBFS Algorithm or not. 
# if two exact environments in forward frontier and backward frontier are found then it's finished.
def end_checker(forward_frontier, backward_frontier):
    for forward_node in forward_frontier:
        for backward_node in backward_frontier:
            if forward_node.environment == backward_node.environment:
                return True, forward_node
    return False, forward_node  # this node is not important.


# creating children in BFS is not the same with IDS. in BFS children are added at the end of the frontier queue
def bfs_forward(node, frontier):
    curr_environment, curr_robot_coordinates, curr_depth = node.environment, node.robot_coordinates, node.depth
    print('*****************')
    print('curr env: \n', node.environment)
    print('curr robot coor \n', node.robot_coordinates)
    all_permitted_movements = get_all_permitted_movements(curr_environment, curr_robot_coordinates)
    print('all permited movements: ', all_permitted_movements)

    for movement in all_permitted_movements:
        new_environment, new_robot_coordinates = update_environment(node.environment, node.robot_coordinates, movement)
        # new states should be checked. they should not be repetetive states.
        if new_environment != node.parent.environment:
            child_node = Node(new_environment, new_robot_coordinates, curr_depth + 1, movement, node)
            frontier.append(child_node)

    print('frontier len is:', len(frontier))
    print_frontier(frontier)
    print('*****************')

    return frontier

# this function return the cell in  environment if we move in the oposite direction of movement. 
def reverse_movement(environment, robot_coordinates, movement, is_goal):
        
    num_rows, num_cols = len(environment), len(environment[0])

    if movement == 'u' and robot_coordinates['x']+1 < num_rows:
        if is_goal:
            environment[robot_coordinates['x']+1][robot_coordinates['y']]  = 'p'
        return environment[robot_coordinates['x']+1][robot_coordinates['y']] 

    elif movement == 'd' and robot_coordinates['x']-1 >= 0:
        if is_goal:
            environment[robot_coordinates['x']-1][robot_coordinates['y']] = 'p'
        return environment[robot_coordinates['x']-1][robot_coordinates['y']] 

    elif movement == 'l' and robot_coordinates['y']+1 < num_cols:
        if is_goal:
            environment[robot_coordinates['x']][robot_coordinates['y']+1] = 'p'
        return environment[robot_coordinates['x']][robot_coordinates['y']+1]

    elif movement == 'r' and robot_coordinates['y']-1 >= 0:
        if is_goal:
            environment[robot_coordinates['x']][robot_coordinates['y']-1] = 'p'
        return environment[robot_coordinates['x']][robot_coordinates['y']-1] 



move_to_coordinate = {'u': {"x": -1}, 'r': {"y": +1}, 'd': {"x": +1}, 'l': {"y": -1}}

# this function updates environment backward (from goal state to initial state).
def update_environment_backward(environment, current_robot_coordinates, movement):

    new_robot_coordinates = dsum(current_robot_coordinates, move_to_coordinate[movement])
    curr_robot_x_coordinate, curr_robot_y_coordinate = current_robot_coordinates['x'], current_robot_coordinates['y']
    new_robot_x_coordinate, new_robot_y_coordinate = new_robot_coordinates['x'], new_robot_coordinates['y']

    new_environment = copy.deepcopy(environment)

    # next robot coordinates have butter
    if new_environment[new_robot_x_coordinate][new_robot_y_coordinate] == 'b':
        new_butter_coordinates = dsum(new_robot_coordinates, move_to_coordinate[movement])
        new_butter_x_coordinate, new_butter_y_coordinate = new_butter_coordinates['x'], new_butter_coordinates['y']

        # next butter coordinates have plate
        if new_environment[new_butter_x_coordinate][new_butter_y_coordinate] == 'p':
            new_environment[new_butter_x_coordinate][new_butter_y_coordinate] = 'bp'
        else:
            new_environment[new_butter_x_coordinate][new_butter_y_coordinate] = 'b'

        new_environment[curr_robot_x_coordinate][curr_robot_y_coordinate] = ''
        new_environment[new_robot_x_coordinate][new_robot_y_coordinate] = 'r'

    # next robot coordinates have plate
    elif new_environment[new_robot_x_coordinate][new_robot_y_coordinate] == 'p':
        new_environment[curr_robot_x_coordinate][curr_robot_y_coordinate] = ''
        new_environment[new_robot_x_coordinate][new_robot_y_coordinate] = 'rp'

    # set new coordinates for butter
    elif reverse_movement(new_environment, current_robot_coordinates, movement, False) == 'b':
        new_environment[curr_robot_x_coordinate][curr_robot_y_coordinate] = 'b'
        new_environment[new_robot_x_coordinate][new_robot_y_coordinate] = 'r'

    # if butter is on goal state
    elif reverse_movement(new_environment, current_robot_coordinates, movement, False) == 'bp':
        reverse_movement(new_environment, current_robot_coordinates, movement, True)
        new_environment[curr_robot_x_coordinate][curr_robot_y_coordinate] = 'b'
        new_environment[new_robot_x_coordinate][new_robot_y_coordinate] = 'r'

    else:
        new_environment[curr_robot_x_coordinate][curr_robot_y_coordinate] = ''
        new_environment[new_robot_x_coordinate][new_robot_y_coordinate] = 'r'

    return new_environment, new_robot_coordinates



def bfs_backward(node, frontier):

    curr_environment, curr_robot_coordinates, curr_depth = node.environment, node.robot_coordinates, node.depth
    print('*****************')
    print('curr env: \n', node.environment)
    print('curr robot coor \n', node.robot_coordinates)
    all_permitted_movements = get_all_permitted_movements(node.environment, node.robot_coordinates)
    print('all permited movements: ', all_permitted_movements)

    for movement in all_permitted_movements:
        # print('loop curr env is: ', node.environment)
        new_environment, new_robot_coordinates = update_environment_backward(node.environment, node.robot_coordinates, movement)
        print('for movement ', movement, 'robot coor is: ',new_robot_coordinates, 'environment is: ', new_environment)
        # new states should be checked. they should not be repetetive states.
        if new_environment != node.parent.environment:
            child_node = Node(new_environment, new_robot_coordinates, curr_depth + 1, movement, node)
            frontier.append(child_node)

    print('backward frontier len is:', len(frontier))
    print_frontier(frontier)
    print('*****************')
    
    return frontier

def create_final_nodes(goal_environments, goal_robots_coordinates):

    backward_frontier = []
    initial_node = Initial_node([])
    for i in range(len(goal_environments)):    # or len(goal_robots_coordinates) it doesn't matter
        backward_frontier.append(Node(goal_environments[i], goal_robots_coordinates[i], 0, ' ', initial_node))

    return backward_frontier


def BBFS(file_name):

    environment_with_cost, environment_without_cost, environment_cost, number_of_butters, robot_coordinates = read_file(file_name)

    forward_frontier, backward_frontier = [], []
    # initialize robot coordinates to initial node
    initial_node = Initial_node([])
    starting_node = Node(environment_without_cost, robot_coordinates, 0, ' ', initial_node)
    forward_frontier.insert(0, starting_node)

    # this function returns all the possible goal states. but it's not enough. nodes are needed for backward bfs.
    goal_environments, goal_robots_coordinates = generate_all_goal_environment(file_name)
    backward_frontier = create_final_nodes(goal_environments, goal_robots_coordinates)

    # create childern of initial node and then create childern in a loop until we reach Goal state
    for i in range(100):
    # while True:
        # if len(forward_frontier) > 0:
        #     forward_frontier = bfs_forward(forward_frontier.pop(0), forward_frontier)

        # backward dfs should be called here
        if len(backward_frontier) > 0:
            backward_frontier = bfs_backward(backward_frontier.pop(0), backward_frontier)

        # environment with no solution should be handled

        is_end, intersected_node = end_checker(forward_frontier, backward_frontier)
        if is_end:
            break

    # find and print final path

    return "path"


if __name__ == '__main__':

    file_name = 'test1.txt'
    s = BBFS(file_name)
    print(s)

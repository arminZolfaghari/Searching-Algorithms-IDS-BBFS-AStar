from collections import defaultdict
import copy


# read file and return information about environment
def read_file(file_name):
    path = "./input/" + file_name
    with open(path, 'r') as file:
        size_rows_cols = file.readline()
        number_of_rows = int(size_rows_cols.split("\t")[0])
        number_of_cols = int(size_rows_cols.split("\t")[1])
        number_of_butter = 0

        matrix_with_cost = []
        matrix_cost = []
        matrix_without_cost = []
        robot_coordinates = {"x": 0, "y": 0}
        for i in range(number_of_rows):
            row = file.readline().replace("\t", " ").replace("\n", "").split(" ")

            row_matrix_with_cost, row_matrix_cost, row_matrix_without_cost = [], [], []
            for j in range(number_of_cols):
                row_matrix_with_cost.append(row[j])

                if row[j].isnumeric():
                    row_matrix_without_cost.append("")
                    row_matrix_cost.append(int(row[j]))
                else:
                    if row[j] == "x":
                        row_matrix_without_cost.append(row[j])
                        row_matrix_cost.append(row[j])
                    else:
                        char = row[j][-1]
                        number = row[j][0:-1]
                        row_matrix_without_cost.append(char)
                        row_matrix_cost.append(int(number))
                        if char == "r":
                            robot_coordinates = {"x": i, "y": j}
                        if char == "b":
                            number_of_butter += 1

            matrix_with_cost.append(row_matrix_with_cost)
            matrix_without_cost.append(row_matrix_without_cost)
            matrix_cost.append(row_matrix_cost)

    return matrix_with_cost, matrix_without_cost, matrix_cost, number_of_butter, robot_coordinates


def move_forward(environment, next_move, robot_coordinates):
    num_rows, num_cols = len(environment), len(environment[0])

    # if next_move == 'u':
    #     robot_coordinates['x'] -= 1
    #
    # elif next_move == 'd':
    #     robot_coordinates['x'] += 1
    #
    # elif next_move == 'r':
    #     robot_coordinates['y'] += 1
    #
    # elif next_move == 'l':
    #     robot_coordinates['y'] -= 1

    new_robot_coordinates = dsum(robot_coordinates, movement_to_coordinate[next_move])

    # robot is not allowed to go outside the environment
    if 0 <= new_robot_coordinates['x'] < num_rows and 0 <= new_robot_coordinates['y'] < num_cols:
        return True, new_robot_coordinates
    else:
        return False, new_robot_coordinates


# def move_backward(next_move, robot_coordinates):
#     if next_move == 'u':
#         robot_coordinates['y'] += 1
#
#     elif next_move == 'd':
#         robot_coordinates['y'] -= 1
#
#     elif next_move == 'r':
#         robot_coordinates['x'] -= 1
#
#     elif next_move == 'l':
#         robot_coordinates['x'] += 1
#
#     return robot_coordinates


# it takes the enviroment, our next move and robot coordinates as input and checks whether the robot can make this
# move or not
def check_next_move(environment, next_move, robot_coordinates):
    is_first_step_available, robot_next_coordinates = move_forward(environment, next_move, robot_coordinates)
    if not is_first_step_available:
        return False

    else:
        # robot is not allowed to go to the cells with x or bp in it
        if 'bp' in environment[robot_next_coordinates['x']][robot_next_coordinates['y']] or 'x' in \
                environment[robot_next_coordinates['x']][robot_next_coordinates['y']]:
            return False

        if 'b' in environment[robot_next_coordinates['x']][robot_next_coordinates['y']]:
            # robot can't push two cells both with butter or after butter cell, cell is x
            is_two_step_available, butter_next_coordinates = move_forward(environment, next_move,
                                                                          robot_next_coordinates)
            if not is_two_step_available:
                return False

            else:
                if 'b' in environment[butter_next_coordinates['x']][butter_next_coordinates['y']]:
                    return False
                if 'x' in environment[butter_next_coordinates['x']][butter_next_coordinates['y']]:
                    return False
                else:
                    return True

        else:
            return True


# get all permitted movements in each state
def get_all_permitted_movements(environment, robot_coordinates):
    all_movements = {'u', 'r', 'd', 'l'}
    all_permitted_movements = []
    for movement in all_movements:
        if check_next_move(environment, movement, robot_coordinates):
            all_permitted_movements.append(movement)

    return all_permitted_movements


movement_to_coordinate = {'u': {"x": -1}, 'r': {"y": +1}, 'd': {"x": +1}, 'l': {"y": -1}}


def dsum(*dicts):
    ret = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k] += v
    return dict(ret)


# get environment and movement then return new environment and new robot coordinates
def update_environment(environment, current_robot_coordinates, movement):
    new_robot_coordinates = dsum(current_robot_coordinates, movement_to_coordinate[movement])
    curr_robot_x_coordinate, curr_robot_y_coordinate = current_robot_coordinates['x'], current_robot_coordinates['y']
    new_robot_x_coordinate, new_robot_y_coordinate = new_robot_coordinates['x'], new_robot_coordinates['y']

    new_environment = copy.deepcopy(environment)

    # next robot coordinates have butter
    if new_environment[new_robot_x_coordinate][new_robot_y_coordinate] == 'b':
        new_butter_coordinates = dsum(new_robot_coordinates, movement_to_coordinate[movement])
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

    elif new_environment[new_robot_x_coordinate][new_robot_y_coordinate] == '' and \
            new_environment[curr_robot_x_coordinate][curr_robot_y_coordinate] == 'rp':
        new_environment[curr_robot_x_coordinate][curr_robot_y_coordinate] = 'p'
        new_environment[new_robot_x_coordinate][new_robot_y_coordinate] = 'r'

    else:
        new_environment[curr_robot_x_coordinate][curr_robot_y_coordinate] = ''
        new_environment[new_robot_x_coordinate][new_robot_y_coordinate] = 'r'

    return new_environment, new_robot_coordinates


def find_plates_coordinates(file_name):
    environment_with_cost, environment_without_cost, environment_cost, number_of_butters, robot_coordinates = read_file(
        file_name)
    num_rows, num_cols = len(environment_without_cost), len(environment_without_cost[0])

    plates_coordinates = []
    for i in range(num_rows):
        for j in range(num_cols):
            if environment_without_cost[i][j] == 'p':
                plates_coordinates.append({"x": i, "y": j})

    return plates_coordinates


def find_butters_coordinates(file_name):
    environment_with_cost, environment_without_cost, environment_cost, number_of_butters, robot_coordinates = read_file(
        file_name)
    num_rows, num_cols = len(environment_without_cost), len(environment_without_cost[0])

    butters_coordinates = []
    for i in range(num_rows):
        for j in range(num_cols):
            if environment_without_cost[i][j] == 'b':
                butters_coordinates.append({"x": i, "y": j})

    return butters_coordinates


def generate_all_goal_environment(file_name):
    environment_with_cost, environment_without_cost, environment_cost, number_of_butters, robot_coordinates = read_file(
        file_name)

    start_robot_x_coordinates, start_robot_y_coordinates = robot_coordinates['x'], robot_coordinates['y']
    all_plates_coordinates = find_plates_coordinates(file_name)

    all_butters_coordinates = find_butters_coordinates(file_name)

    for plate_coordinates in all_plates_coordinates:
        plate_x_coordinate, plate_y_coordinate = plate_coordinates['x'], plate_coordinates['y']
        environment_without_cost[plate_x_coordinate][plate_y_coordinate] = "bp"

    for butter_coordinates in all_butters_coordinates:
        butter_x_coordinate, butter_y_coordinate = butter_coordinates['x'], butter_coordinates['y']
        environment_without_cost[butter_x_coordinate][butter_y_coordinate] = ''

    all_final_robot_coordinates = []
    for plate_coordinates in all_plates_coordinates:
        plate_x_coordinate, plate_y_coordinate = plate_coordinates['x'], plate_coordinates['y']
        all_permitted_movements = get_all_permitted_movements(environment_without_cost, plate_coordinates)
        for movement in all_permitted_movements:
            final_robot_coordinates = dsum(plate_coordinates, movement_to_coordinate[movement])
            all_final_robot_coordinates.append(final_robot_coordinates)

    environment_without_cost[start_robot_x_coordinates][start_robot_y_coordinates] = ""
    all_goal_environment = []
    all_goal_robot_coordinates = []
    for final_robot_coordinates in all_final_robot_coordinates:
        goal_environment = copy.deepcopy(environment_without_cost)
        final_robot_x_coordinates, final_robot_y_coordinates = final_robot_coordinates['x'], final_robot_coordinates[
            'y']
        goal_environment[final_robot_x_coordinates][final_robot_y_coordinates] = 'r'
        all_goal_environment.append(goal_environment)
        all_goal_robot_coordinates.append(final_robot_coordinates)

    return all_goal_environment, all_goal_robot_coordinates


# get final node(goal state) and return path from start node to goal node
def find_path_with_final_node(node):
    path_by_nodes = []
    pre_node = node

    while pre_node != "":
        path_by_nodes.append(pre_node)
        pre_node = pre_node.parent

    path_by_nodes.reverse()
    return path_by_nodes


if __name__ == "__main__":
    arr1, arr2 = generate_all_goal_environment("test6.txt")
    for i in arr1:
        print(i)

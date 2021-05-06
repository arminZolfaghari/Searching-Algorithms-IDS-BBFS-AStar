from collections import defaultdict


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
                    row_matrix_cost.append(row[j])
                else:
                    if row[j] == "x":
                        row_matrix_without_cost.append(row[j])
                        row_matrix_cost.append(row[j])
                    else:
                        char = row[j][-1]
                        number = row[j][0:-1]
                        row_matrix_without_cost.append(char)
                        row_matrix_cost.append(number)
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

    if next_move == 'u':
        robot_coordinates['x'] -= 1

    elif next_move == 'd':
        robot_coordinates['x'] += 1

    elif next_move == 'r':
        robot_coordinates['y'] += 1

    elif next_move == 'l':
        robot_coordinates['y'] -= 1

    robot_new_coordinates = {"x": robot_coordinates['x'], "y": robot_coordinates["y"]}
    # robot is not allowed to go outside the environment
    if 0 <= robot_new_coordinates['x'] < num_rows and 0 <= robot_new_coordinates['y'] < num_cols:
        print(next_move)
        print(robot_new_coordinates)
        return True, robot_new_coordinates
    else:
        return False, robot_new_coordinates


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
    num_rows, num_cols = len(environment), len(environment[0])

    is_first_step_available, robot_next_coordinates = move_forward(environment, next_move, robot_coordinates)
    if not is_first_step_available:
        return False

    else:
        # robot is not allowed to go to the cells with x or p in it
        if ('x' or 'p' or 'rp') in environment[robot_next_coordinates.get('x')][robot_next_coordinates.get('y')]:
            return False

        # robot can't push two cells both with butter or after butter cell, cell is x
        is_two_step_available, robot_2next_coordinates = move_forward(environment, next_move, robot_next_coordinates)
        if is_two_step_available:
            if 'b' in environment[robot_next_coordinates['x']][robot_next_coordinates['y']] and 'b' in environment[
                robot_2next_coordinates['x']][robot_2next_coordinates['y']]:
                return False
            if 'b' in environment[robot_next_coordinates['x']][robot_next_coordinates['y']] and 'x' in environment[
                robot_2next_coordinates['x'][robot_2next_coordinates['y']]]:
                return False

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

    # next robot coordinates have butter
    if environment[new_robot_x_coordinate][new_robot_y_coordinate] == 'b':
        new_butter_coordinates = dsum(new_robot_coordinates, movement_to_coordinate[movement])
        new_butter_x_coordinate, new_butter_y_coordinate = new_butter_coordinates['x'], new_butter_coordinates['y']

        # next butter coordinates have plate
        if environment[new_butter_x_coordinate][new_butter_y_coordinate] == 'p':
            environment[new_butter_x_coordinate][new_butter_y_coordinate] = 'bp'
        else:
            environment[new_butter_x_coordinate][new_butter_y_coordinate] = 'b'

    environment[curr_robot_x_coordinate][curr_robot_y_coordinate] = ''
    environment[new_robot_x_coordinate][new_robot_y_coordinate] = 'r'

    return environment, new_robot_coordinates


def find_plates_coordinates():
    environment_with_cost, environment_without_cost, environment_cost, number_of_butters, robot_coordinates = read_file(
        "test1.txt")
    num_rows, num_cols = len(environment_without_cost), len(environment_without_cost[0])

    plates_coordinates = []
    for i in range(num_rows):
        for j in range(num_cols):
            if environment_without_cost[i][j] == 'p':
                plates_coordinates.append({"x": i, "y": j})

    return plates_coordinates


def find_butters_coordinates():
    environment_with_cost, environment_without_cost, environment_cost, number_of_butters, robot_coordinates = read_file(
        "test1.txt")
    num_rows, num_cols = len(environment_without_cost), len(environment_without_cost[0])

    plates_coordinates = []
    for i in range(num_rows):
        for j in range(num_cols):
            if environment_without_cost[i][j] == 'b':
                plates_coordinates.append({"x": i, "y": j})

    return plates_coordinates


def generate_all_goal_environment():
    environment_with_cost, environment_without_cost, environment_cost, number_of_butters, robot_coordinates = read_file(
        "test1.txt")
    print(environment_without_cost)
    start_robot_x_coordinates, start_robot_y_coordinates = robot_coordinates['x'], robot_coordinates['y']
    all_plates_coordinates = find_plates_coordinates()
    print(all_plates_coordinates)
    all_butters_coordinates = find_butters_coordinates()
    print(all_butters_coordinates)

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
        print(all_permitted_movements)
        for movement in all_permitted_movements:
            final_robot_coordinates = dsum(plate_coordinates, movement_to_coordinate[movement])
            all_final_robot_coordinates.append(final_robot_coordinates)

    environment_without_cost[start_robot_x_coordinates][start_robot_y_coordinates] = ""
    all_goal_environment = []
    for final_robot_coordinates in all_final_robot_coordinates:
        goal_environment = environment_without_cost
        final_robot_x_coordinates, final_robot_y_coordinates = final_robot_coordinates['x'], final_robot_coordinates[
            'y']
        print(final_robot_coordinates)
        goal_environment[final_robot_x_coordinates][final_robot_y_coordinates] = 'r'
        all_goal_environment.append(goal_environment)

    return all_goal_environment


if __name__ == "__main__":
    arr = generate_all_goal_environment()
    print(arr)

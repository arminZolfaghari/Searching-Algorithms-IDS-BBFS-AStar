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
                    row_matrix_without_cost.append("1")
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
        robot_coordinates['y'] -= 1

    elif next_move == 'd':
        robot_coordinates['y'] += 1

    elif next_move == 'r':
        robot_coordinates['x'] += 1

    elif next_move == 'l':
        robot_coordinates['x'] -= 1

    # robot is not allowed to go outside the environment
    if 0 <= robot_coordinates['x'] <= num_rows and 0 <= robot_coordinates['y'] <= num_cols:
        return True, robot_coordinates
    else:
        return False, robot_coordinates


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

    # robot is not allowed to go to the cells with x in it
    elif 'x' in environment[robot_next_coordinates.get('x')][robot_next_coordinates.get('y')]:
        return False

    # robot can't push two cells both with butter
    is_two_step_available, robot_2next_coordinates = move_forward(environment, next_move, robot_next_coordinates)
    if is_two_step_available:
        if 'b' in environment[robot_next_coordinates['x']][robot_next_coordinates['y']] and 'b' in environment[robot_2next_coordinates['x'][robot_2next_coordinates['y']]]:
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

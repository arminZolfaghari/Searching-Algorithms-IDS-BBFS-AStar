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

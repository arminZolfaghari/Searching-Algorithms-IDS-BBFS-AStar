def move_forward(next_move, robot_coordinates):

    if next_move == 'u':
        robot_coordinates['y'] += 1

    elif next_move == 'd':
        robot_coordinates['y'] -= 1

    elif next_move == 'r':
        robot_coordinates['x'] += 1

    elif next_move == 'l':
        robot_coordinates['x'] -= 1

    return robot_coordinates

def move_backward(next_move, robot_coordinates):

    if next_move == 'u':
        robot_coordinates['y'] -= 1

    elif next_move == 'd':
        robot_coordinates['y'] += 1

    elif next_move == 'r':
        robot_coordinates['x'] -= 1

    elif next_move == 'l':
        robot_coordinates['x'] += 1

    return robot_coordinates


# it takes the enviroment, our next move and robot coordinates as input and checks whether the robot can make this move or not
def check_next_move(enviroment, next_move, robot_coordinates):

    num_rows, num_cols = len(enviroment), len(enviroment[0])
    robot_coordinates = move_forward(next_move, robot_coordinates)

    # robot is not allowed to go outside the enviroment
    if robot_coordinates.get('x') > num_rows or robot_coordinates.get('y') > num_cols:
        robot_coordinates = move_backward(next_move, robot_coordinates)
        return False

    # robot is not allowed to go to the cells with x in it
    elif True:
        pass

    # robot can't push two cells both with butter
    elif True:
        pass
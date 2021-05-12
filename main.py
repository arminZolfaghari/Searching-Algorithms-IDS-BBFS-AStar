import IterativeDeepeningSearch as ids
import BidirectionalBreadthFirstSearch as bbfs
import AStar as astar
import GraphicalInterface as gui
import AdditionalFunctions as funcs
import time



if __name__ == "__main__":

    file_name = 'test4.txt'

    # IDS Algorithm
    # ids.start_ids_algorithm("test1.txt", 15)


    # BBFS ALgorithm
    start_time = time.time()
    has_result, path = bbfs.BBFS(file_name)
    finish_time = time.time()
    duration = (finish_time - start_time)
    if not has_result:
        print('there is no answer in this environment!')
    else:
        movement_list = funcs.find_movement_list(path)
        print('path length is: ', len(path))
        print('path is: ', movement_list)
        funcs.print_path(path)
        g = gui.GraphicalInterface(path)
        g.Visualize()
        # funcs.write_to_file("BBFS", file_name, movement_list, duration)


    # A* Algorithm
    # start_time = time.time()
    # has_result, path, goal_depth = astar.start_a_star_algorithm(file_name, 35)
    # finish_time = time.time()
    # duration = (finish_time - start_time)
    # if not has_result:
    #     print('there is no answer in this environment!')
    # else:
    #     movement_list = funcs.find_movement_list(path)
    #     print("path costs : ", path[-1].cost_g)
    #     print("depth of goal : ", goal_depth)
    #     funcs.print_path(path)
        # g = gui.GraphicalInterface(path)
        # g.Visualize()
        # funcs.write_to_file("ASTAR", file_name, movement_list, duration)



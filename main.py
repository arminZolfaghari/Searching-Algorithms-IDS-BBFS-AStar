import IterativeDeepeningSearch as ids
import BidirectionalBreadthFirstSearch as bbfs
import AStar as astar
import GraphicalInterface as gui
import AdditionalFunctions as funcs
import time

if __name__ == "__main__":
    file_name = 'test3.txt'
    algorithm = input("Which Algorithm do you want to use?\n1) IDS\n2) BBFS\n3) A*\n")

    if algorithm == "1" or algorithm == "IDS":
        start_time = time.time()
        has_result, path, goal_depth, nodes_info = ids.start_ids_algorithm(file_name, 15)
        finish_time = time.time()
        duration = (finish_time - start_time)
        print("number of created nodes are:", nodes_info[0])
        print("number of expanded nodes are:", nodes_info[1])
        print("duration is : ", duration)

        if not has_result:
            print('there is no answer in this environment!')
        else:
            movement_list = funcs.find_movement_list(path)
            print("path costs : ", path[-1].cost_g)
            print("depth of goal : ", goal_depth)
            print('path is: ', movement_list)
            funcs.print_path(path)
            g = gui.GraphicalInterface(path)
            g.Visualize()
            funcs.write_to_file("IDS", file_name, movement_list, duration)


    elif algorithm == "2" or algorithm == "BBFS":
        start_time = time.time()
        has_result, path, nodes_info = bbfs.BBFS(file_name)
        finish_time = time.time()
        duration = (finish_time - start_time)
        print("number of created nodes are:", nodes_info[0])
        print("number of expanded nodes are:", nodes_info[1])
        print("duration is : ", duration)


        if not has_result:
            print('there is no answer in this environment!')
        else:
            movement_list = funcs.find_movement_list(path)
            print('depth of goal : ', len(path) - 1)
            print('path is: ', movement_list)
            funcs.print_path(path)
            g = gui.GraphicalInterface(path)
            g.Visualize()
            # funcs.write_to_file("BBFS", file_name, movement_list, duration)

    elif algorithm == "3" or algorithm == "A*":
        start_time = time.time()
        has_result, path, goal_depth, nodes_info = astar.start_a_star_algorithm(file_name, 20)
        finish_time = time.time()
        duration = (finish_time - start_time)

        print("number of created nodes are:", nodes_info[0])
        print("number of expanded nodes are:", nodes_info[1])
        print("duration is : ", duration)

        if not has_result:
            print('there is no answer in this environment!')
        else:
            movement_list = funcs.find_movement_list(path)
            print("path costs : ", path[-1].cost_g)
            print("depth of goal : ", goal_depth)
            print('path is: ', movement_list)
            funcs.print_path(path)
            g = gui.GraphicalInterface(path)
            g.Visualize()
            funcs.write_to_file("ASTAR", file_name, movement_list, duration)

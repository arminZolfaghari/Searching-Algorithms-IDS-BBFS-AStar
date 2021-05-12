import IterativeDeepeningSearch as ids
import BidirectionalBreadthFirstSearch as bbfs
import AStar as astar
import GraphicalInterface as gui



if __name__ == "__main__":

    file_name = 'test1.txt'

    # IDS Algorithm
    ids.start_ids_algorithm("test1.txt", 15)



    # BBFS ALgorithm
    # path = bbfs.BBFS(file_name)
    # movement_list = []
    # if path == ['no answer']:
    #     print('there is no answer in this environment!')
    # else:
    #     for p in path:
    #         movement_list.append(p.movement)
    #     movement_list.pop(0)
    #     print('path length is: ', len(path))
    #     print('path is: ', movement_list)
    #     bbfs.print_path(path)
    #     g = gui.GraphicalInterface(path)
    #     g.Visualize()
        # write_to_file(file_name, movement_list, duration)


    # A* Algorithm
    result, path, goal_depth = astar.start_a_star_algorithm("test5.txt", 35)
    print("result : ", result)
    print("path costs : ", path[-1].cost_g)
    print(path)         # pass the gui
    print("depth of goal : ", goal_depth)
    g = gui.GraphicalInterface(path)
    g.Visualize()


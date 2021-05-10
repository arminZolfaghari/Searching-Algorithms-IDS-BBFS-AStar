from AdditionalFunctions import *
from Node import *
import time
import copy


def calculate_manhattan_distance(point1, point2):
    x_point1, y_point1 = point1['x'], point1['y']
    x_point2, y_point2 = point2['x'], point2['y']

    return abs(x_point1 - x_point2) + abs(y_point1 - y_point2)


def find_butter_for_plate(butters_coordinates_arr, plates_coordinates_arr):
    butters_arr_sorted = []
    plates_arr_sorted = []
    for butter_coordinates in butters_coordinates_arr:
        res_plate = plates_coordinates_arr[0]
        min_distance = calculate_manhattan_distance(butter_coordinates, res_plate)
        for plate_coordinates in plates_coordinates_arr:
            distance = calculate_manhattan_distance(butter_coordinates, plate_coordinates)
            if min_distance > distance:
                res_plate = plate_coordinates

        butters_arr_sorted.append(butter_coordinates)
        plates_arr_sorted.append(res_plate)
        plates_coordinates_arr.remove(res_plate)

    return butters_arr_sorted, plates_arr_sorted


def find_closest_plate(now_coordinates, plates_coordinates):
    distance_arr = []
    for plate_coordinates in plates_coordinates:
        distance_arr.append(calculate_manhattan_distance(now_coordinates, plate_coordinates))

    best_plate_index = distance_arr.index(min(distance_arr))
    best_plate = plates_coordinates[best_plate_index]
    return best_plate


def calculate_distance_point_to_all_plates(point, plates_coordinates_arr):
    distance = 0
    point_copy = point
    plates_coordinates_arr_copy = copy.deepcopy(plates_coordinates_arr)
    while plates_coordinates_arr_copy:
        best_plate = find_closest_plate(point_copy, plates_coordinates_arr_copy)
        plates_coordinates_arr_copy.remove(best_plate)
        distance += calculate_manhattan_distance(point_copy, best_plate)
        # print(point_copy)
        # print(best_plate)
        # print(distance)
        point_copy = best_plate
    # print("***************")

    return distance


def calculate_heuristic_environment(plates_coordinates_arr, environment_without_cost):
    num_rows, num_cols = len(environment_without_cost), len(environment_without_cost[0])
    heuristic_environment = [[0 for i in range(num_cols)] for j in range(num_rows)]

    for i in range(num_rows):
        for j in range(num_cols):
            heuristic_environment[i][j] = calculate_distance_point_to_all_plates({"x": i, "y": j},
                                                                                 plates_coordinates_arr)

    return heuristic_environment


# calculate_heuristic 2
# def calculate_heuristic(point, butters_coordinates_arr, plates_coordinates_arr):
#     butters_arr_sorted, plates_arr_sorted = find_butter_for_plate(butters_coordinates_arr, plates_coordinates_arr)
#


if __name__ == "__main__":
    environment_without_cost = read_file("test3.txt")[1]
    print(environment_without_cost)
    arr_plates = find_plates_coordinates("test3.txt")
    print(arr_plates)

    print(calculate_heuristic_environment(arr_plates, environment_without_cost))

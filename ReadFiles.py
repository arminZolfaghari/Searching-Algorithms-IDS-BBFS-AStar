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


if __name__ == "__main__":
    matrix_with_cost, matrix_without_cost, matrix_cost, number_of_butter, robot = read_file("test2.txt")
    print(matrix_with_cost)
    print(matrix_without_cost)
    print(matrix_cost)
    print(number_of_butter)
    print(robot)

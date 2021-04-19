def read_file_to_arr(file_name):
    path = "./input/" + file_name
    with open(path, 'r') as file:
        size_rows_cols = file.readline()
        number_of_rows = int(size_rows_cols.split("\t")[0])
        number_of_cols = int(size_rows_cols.split("\t")[1])
        print(number_of_cols)
        print(number_of_cols)
        arr = []
        for i in range(number_of_rows):
            row = file.readline().replace("\t", " ").replace("\n", "").split(" ")
            row_arr = []
            for j in range(number_of_cols):
                row_arr.append(row[j])
            arr.append(row_arr)
    return arr


if __name__ == "__main__":
    arr_input1 = read_file_to_arr("test1.txt")
    print(arr_input1)

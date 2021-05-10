import tkinter as tk
from tkinter import ttk
import time

root = tk.Tk()

class GraphicalInterface():

    def __init__(self, path):
        self.path = path
        self.Visualize(path, 0)
        root.mainloop()


    def Visualize(self, path, step):

        num_rows, num_cols = len(path[0].environment), len(path[0].environment[0])
        WIDTH = num_cols * 100
        HEIGHT = num_rows * 100   
        root.geometry(f"{WIDTH}x{HEIGHT}")
        root.title('Path Finding!')
        # root.resizable(0, 0)

        root.columnconfigure(0, weight=num_cols)
        root.columnconfigure(1, weight=num_rows)

        if step < len(path):
            for r in range(num_rows):
                for c in range(num_cols):

                    if path[step].environment[r][c] == "x":
                        photo = tk.PhotoImage(file='./Assets/x.png')
                        label = ttk.Label(root, image=photo)
                        label.grid(column=c, row=r, padx=5, pady=5)
                        
                    elif path[step].environment[r][c] == "":
                        label = ttk.Label(root, text="cell")
                        label.grid(column=c, row=r, padx=5, pady=5)
                        
                    elif path[step].environment[r][c] == "r":
                        photo = tk.PhotoImage(file='./Assets/robot.png')
                        label = ttk.Label(root, image=photo)
                        label.grid(column=c, row=r, padx=5, pady=5) 

                    elif path[step].environment[r][c] == "p":
                        photo = tk.PhotoImage(file='./Assets/plate.png')
                        label = ttk.Label(root, image=photo)
                        label.grid(column=c, row=r, padx=5, pady=5)
                        
                    elif path[step].environment[r][c] == "b":
                        photo = tk.PhotoImage(file='./Assets/butter2.png')
                        label = ttk.Label(root, image=photo)
                        label.grid(column=c, row=r, padx=5, pady=5)
                        

            step += 1

            root.after(400, self.Visualize(path, step+1))
        root.mainloop()


import BBFS as b
if __name__ == "__main__":

    file_name = 'test1.txt'
    path = b.BBFS(file_name)
    movement_list = []
    for p in path:
        movement_list.append(p.movement)
    movement_list.pop(0)
    print('path length is: ', len(path))
    print('path is: ', movement_list)
    b.print_path(path)
    g = GraphicalInterface(path)

import tkinter as tk
from tkinter import ttk
import time
from PIL import ImageTk, Image

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
        root.configure(bg='white')
        # root.resizable(0, 0)

        root.columnconfigure(0, weight=num_cols)
        root.columnconfigure(1, weight=num_rows)

        x_image = ImageTk.PhotoImage(Image.open('./Assets/x.png').resize((100, 100),Image.ANTIALIAS))
        cell_image = ImageTk.PhotoImage(Image.open('./Assets/cell.png').resize((100, 100),Image.ANTIALIAS))
        robot_image = ImageTk.PhotoImage(Image.open('./Assets/robot.png').resize((100, 100),Image.ANTIALIAS))
        plate_image = ImageTk.PhotoImage(Image.open('./Assets/plate.png').resize((100, 100),Image.ANTIALIAS))
        butter_image = ImageTk.PhotoImage(Image.open('./Assets/butter.png').resize((100, 100),Image.ANTIALIAS))

        if step < len(path):
            for r in range(num_rows):
                for c in range(num_cols):

                    if path[step].environment[r][c] == "x":
                        label = ttk.Label(root, image=x_image)
                        label.grid(column=c, row=r)
                        
                    elif path[step].environment[r][c] == "":
                        label = ttk.Label(root, image=cell_image)
                        label.grid(column=c, row=r)
                        
                    elif path[step].environment[r][c] == "r" or path[step].environment[r][c] == "rp":
                        label = ttk.Label(root, image=robot_image)
                        label.grid(column=c, row=r) 

                    elif path[step].environment[r][c] == "b" or path[step].environment[r][c] == "bp":
                        label = ttk.Label(root, image=butter_image)
                        label.grid(column=c, row=r)

                    elif path[step].environment[r][c] == "p":
                        label = ttk.Label(root, image=plate_image)
                        label.grid(column=c, row=r)
                        

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

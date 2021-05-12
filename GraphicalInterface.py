import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

root = tk.Tk()

class GraphicalInterface():

    def __init__(self, path):
        self.path = path
        self.step = 0
        self.Visualize()

    def Visualize(self, e=1):

        num_rows, num_cols = len(self.path[0].environment), len(self.path[0].environment[0])
        WIDTH = (num_cols * 100) + 10
        HEIGHT = (num_rows * 100) + 10   
        root.geometry(f"{WIDTH}x{HEIGHT}")
        root.title('Path Finding!')
        root.configure(bg='white')

        root.columnconfigure(0, weight=num_cols)
        root.columnconfigure(1, weight=num_rows)

        x_image = ImageTk.PhotoImage(Image.open('./Assets/x.png').resize((100, 100),Image.ANTIALIAS))
        cell_image = ImageTk.PhotoImage(Image.open('./Assets/cell.png').resize((100, 100),Image.ANTIALIAS))
        robot_image = ImageTk.PhotoImage(Image.open('./Assets/robot.png').resize((100, 100),Image.ANTIALIAS))
        plate_image = ImageTk.PhotoImage(Image.open('./Assets/plate.png').resize((100, 100),Image.ANTIALIAS))
        butter_image = ImageTk.PhotoImage(Image.open('./Assets/butter.png').resize((100, 100),Image.ANTIALIAS))

        if self.step < len(self.path):
            for r in range(num_rows):
                for c in range(num_cols):

                    if self.path[self.step].environment[r][c] == "x":
                        label = ttk.Label(root, image=x_image)
                        label.grid(column=c, row=r)
                        
                    elif self.path[self.step].environment[r][c] == "":
                        label = ttk.Label(root, image=cell_image)
                        label.grid(column=c, row=r)
                        
                    elif self.path[self.step].environment[r][c] == "r" or self.path[self.step].environment[r][c] == "rp":
                        label = ttk.Label(root, image=robot_image)
                        label.grid(column=c, row=r) 

                    elif self.path[self.step].environment[r][c] == "b" or self.path[self.step].environment[r][c] == "bp":
                        label = ttk.Label(root, image=butter_image)
                        label.grid(column=c, row=r)

                    elif self.path[self.step].environment[r][c] == "p":
                        label = ttk.Label(root, image=plate_image)
                        label.grid(column=c, row=r)

            self.step += 1
            root.after(1000, self.Visualize)
        root.mainloop()
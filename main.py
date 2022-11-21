import tkinter as tk
from gui import Window
from db import DataBase

# Creating the base for GUI
root = tk.Tk()
# Establishing DB connection
db = DataBase()
# Building the interface
Window(db, root)
# Looping the interface
root.mainloop()

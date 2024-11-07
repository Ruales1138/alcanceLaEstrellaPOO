import tkinter as tk
from interface.graphic_interface import GraphicInterface

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicInterface(root)
    root.mainloop()
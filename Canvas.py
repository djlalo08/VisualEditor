import tkinter as tk
from Point import Point


class Canvas(tk.Frame):
    canvas_width = 1500
    canvas_height = 1000
    root = None
    canvas = None

    _drag_data = {"pos": Point(0,0), "item": None}
    selected = None
    mode = "select"
    id_map = {}
    map_count = 0
    ins = []
    outs = []
        
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Canvas.canvas = tk.Canvas(width=canvas_width, height=canvas_height, background="#f5ecce")
        Canvas.canvas = tk.Canvas(width=Canvas.canvas_width, height=Canvas.canvas_height, background="white")
        Canvas.canvas.pack(fill="both", expand=True)
        Canvas.root = parent

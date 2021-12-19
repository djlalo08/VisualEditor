from __future__ import annotations
import tkinter as tk
import ObjectHierarchy.Object as O
from Point import Point
from Wire import InputWire, OutputWire


class Canvas(tk.Frame):
    canvas_width = 1500
    canvas_height = 1000
    root = None
    canvas = None

    _drag_data = {"pos": Point(0,0), "item": None}
    selected = None
    mode = "select"
    id_map: dict[int, O.Object]= {}
    map_count = 0
    ins: list[InputWire] = []
    outs: list[OutputWire] = []
        
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Canvas.canvas = tk.Canvas(width=canvas_width, height=canvas_height, background="#f5ecce")
        Canvas.canvas = tk.Canvas(width=Canvas.canvas_width, height=Canvas.canvas_height, background="white")
        Canvas.canvas.pack(fill="both", expand=True)
        Canvas.root = parent
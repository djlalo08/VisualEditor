from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ObjectHierarchy.Object import Object
    from Wire import InputWire, OutputWire

from Point import Point


class EditorWindow(tk.Frame):
    canvas_width = 600
    canvas_height = 600
    root = None
    canvas : tk.Canvas

    _drag_data = {"pos": Point(0,0), "item": None}
    selected: Object | None = None
    selected_index: int = 0
    file_name:str = ''
    mode: str = "select"
    id_map: dict[int, Object]= {}
    map_count : int = 0
    ins: list[InputWire] = []
    outs: list[OutputWire] = []
        
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        EditorWindow.canvas = tk.Canvas(background="#f5ecce")
        EditorWindow.canvas.pack(fill="both", expand=True)
        EditorWindow.root = parent

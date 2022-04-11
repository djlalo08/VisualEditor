import tkinter as tk
from Bindings.Nester import Nester
from Point import Point
from Canvas import Canvas
from Function import Function
from MapData import MapData

class MapModal(tk.Toplevel):
    def __init__(self, cursorPos=Point(200,200), insert_into=None) -> None:
        super().__init__(Canvas.root)
        self.cursorPos = cursorPos
        self.fn_name = tk.StringVar()
        self.ins = tk.StringVar()
        self.outs = tk.StringVar()
        self.hide_outs = tk.BooleanVar()
        self.insert_into = insert_into
        self.new_map_modal()
        self.bind('<Return>', self.submit)

    def submit(self, event=None):
        fn_name = self.fn_name.get()
        ins = self.ins.get().split(",")
        outs = self.outs.get().split(",")
        result_map = self.add_map(self.cursorPos, fn_name, ins, outs, self.hide_outs.get())
        if self.insert_into:
            Nester.drag_map_into_node(result_map)
        self.destroy()
            
    @staticmethod
    def add_map(pos=Point(200,200), fn_name="map", ins=["int"], outs=["int"], hide_outs=False):
        fn = Function(fn_name, ins, outs)
        return MapData(pos=pos, name=fn_name, fn=fn, hide_outs=hide_outs)
        
    def new_map_modal(self):
        self.title("Set map info")
        self.geometry("460x180")

        fn_name_label = tk.Label(self, text = "fn name").place(x = 40, y = 20)  
        fn_name = tk.Entry(self, width = 30, textvariable=self.fn_name).place(x = 110, y = 20)  

        in_label = tk.Label(self, text = "ins").place(x = 40, y = 60)  
        ins = tk.Entry(self, width = 30, textvariable=self.ins).place(x = 110, y = 60)  

        out_label = tk.Label(self, text = "outs").place(x = 40, y = 100)  
        outs = tk.Entry(self, width = 30, textvariable=self.outs).place(x = 110, y = 100)  

        out_label = tk.Label(self, text = "hide_outs").place(x = 40, y = 140)  
        outs = tk.Checkbutton(self, width = 30, variable=self.hide_outs).place(x = 110, y = 140)  

        submit_button = tk.Button(self, text = "Give me a map!", command=self.submit).place(x = 250, y = 140)
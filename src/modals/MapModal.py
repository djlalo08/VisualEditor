import pickle
import tkinter as tk

from EditorWindow import EditorWindow
from GlobalData import resources
from MapData import MapData
from Point import Point
from actors.nester import Nester


class MapModal(tk.Toplevel):
    def __init__(self, cursor_pos=Point(200, 200), insert_into=None, enclose=None) -> None:
        super().__init__(EditorWindow.root)
        self.cursorPos = cursor_pos
        self.fn_name = tk.StringVar()
        self.insert_into = insert_into
        self.enclose = enclose
        self.new_map_modal()
        self.bind('<Return>', self.submit)
        self.bind('<Escape>', self.exit)

    def submit(self, event=None):
        result_map = self.add_map(self.cursorPos, self.fn_name.get())

        if self.insert_into:
            Nester.drag_map_into_node(result_map)
        if self.enclose:
            node_pos = result_map.input_nodes[0].abs_pos()
            enclosed_pos = self.enclose.abs_pos()
            self.enclose.move(node_pos - enclosed_pos)
            Nester.drag_map_into_node(self.enclose)

        result_map.update()
        self.exit()

    def exit(self, event=None):
        self.destroy()

    @staticmethod
    def add_map(pos=Point(200, 200), fn_name="map"):
        with open(f'{resources}/lib/int/{fn_name}.Int', 'rb') as file:
            interface = pickle.load(file)
            return MapData(interface, pos=pos)

    def new_map_modal(self):
        self.title("")
        x = EditorWindow.root.winfo_x()
        y = EditorWindow.root.winfo_y()
        (dx, dy) = self.cursorPos.unpack()
        (w, h) = (195, 30)
        self.geometry("%dx%d+%d+%d" % (w, h, x + dx, y + dy))

        fn_name = tk.Entry(self, textvariable=self.fn_name)
        fn_name.place(x=0, y=0)
        fn_name.focus()

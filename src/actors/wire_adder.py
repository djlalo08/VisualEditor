from os import stat
from EditorWindow import EditorWindow
from utils.canvas import cursorxy
from Point import Point
from Wire import InputWire, OutputWire, Wire


class WireAdder:

    @staticmethod
    def add_in_wire(event=None):
        i = len(EditorWindow.ins)
        x = i*40+200
        points = [Point(x, 30), Point(x, 80), Point(x, 120)]
        wire = InputWire(points=points, index=i)
        EditorWindow.ins += [wire]

    @staticmethod
    def remove_in_wire(event):
        # TODO
        pass

    @staticmethod
    def add_out_wire(event=None):
        i = len(EditorWindow.outs)
        x = i*20+200
        points = [Point(x, EditorWindow.canvas_height-30), 
                  Point(x, EditorWindow.canvas_height-80), 
                  Point(x, EditorWindow.canvas_height-250)]
        wire = OutputWire(points=points, index=i)
        EditorWindow.outs += [wire]

    @staticmethod
    def remove_out_wire(event):
        # TODO
        pass

    @staticmethod
    def add_free_wire(event):
        (x, y) = cursorxy()
        wire = Wire(points=[Point(x, y), Point(x, y+50)])
        wire.update()
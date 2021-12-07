from Point import Point
from MapNode import *
from Function import Function
from Object import Object
from Tree import Node

class MapData(Object):
    def __init__(self, canvas, width=100, height=100, ins=None, outs=None, fn=Function(), name="name", **kwargs) -> None:
        super().__init__(canvas, width=width, height=height, **kwargs)
        self.fn = fn
        self.name = name
        self.ins = ins if ins != None else [None]*len(fn.input_types)
        self.outs = outs if outs != None else [None]*len(fn.output_types)
        self.children = self._create_children()
        
    def build_obj(self):
        return self.canvas.create_rectangle(
            self.abs_pos().around(self.width, self.height),
            outline="black",
            fill="gold",
            tags=("draggable", ),
        )

    def _create_children(self):
        children = []
        for index, _ in enumerate(self.fn.input_types):
            children.append(MapInputNode(self.canvas, self, index, offset=self.abs_pos()))

        for index, _ in enumerate(self.fn.output_types):
            children.append(MapOutputNode(self.canvas, self, index, offset=self.abs_pos()))

        return children
    
    def get_value(self):
        in_values = []
        for input in self.ins:
            input_val = input.get_value()
            in_values.append(input_val)
            
        return Node((self.fn.name, self.id), in_values)
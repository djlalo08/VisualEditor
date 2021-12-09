from Label import Label
from MapNode import *
from Function import Function
from ObjectHierarchy.Object import Object
from Tree import Node

class MapData(Object):
    def __init__(self, *args, width=100, ins=None, outs=None, fn=Function(), name="name", **kwargs) -> None:
        self.fn = fn
        self.name = name
        self.ins = ins if ins != None else [None]*len(fn.input_types)
        self.outs = outs if outs != None else [None]*len(fn.output_types)
        self.height = max(len(self.ins), len(self.outs))*20+10
        super().__init__(*args, width=width, height=self.height, **kwargs)
        self.children = self._create_children()
        
    def build_obj(self):
        return Canvas.canvas.create_rectangle(
            self.abs_pos().around(self.width, self.height),
            outline="black",
            fill="#E7B680",
            tags=("draggable", ),
        )

    def _create_children(self):
        children = []
        for index, _ in enumerate(self.fn.input_types):
            children.append(MapInputNode(self, index, offset=self.abs_pos(), offset_off_parent=Point(0,-self.height/2+5)))

        for index, _ in enumerate(self.fn.output_types):
            children.append(MapOutputNode(self, index, offset=self.abs_pos(), offset_off_parent=Point(0,-self.height/2+5)))
            
        children.append(Label(self, self.name, offset=self.abs_pos())) 

        return children
    
    def get_value(self):
        in_values = []
        for input in self.ins:
            input_val = input.get_value()
            in_values.append(input_val)
            
        return Node((self.fn.name, self.id), in_values)
from __future__ import annotations
from Label import Label
from MapNode import MapInputNode, MapNode, MapOutputNode
from Function import Function
from ObjectHierarchy.Object import Object
from Tree import Node
from ObjectHierarchy.ObjectReference import ObjectReference
from Canvas import Canvas
from Point import Point

class MapData(Object):
    def __init__(self, *args, width=100, ins=None, outs=None, fn=Function(), name="name", **kwargs) -> None:
        self.fn = fn
        self.name = name
        self.ins = ins if ins != None else [None]*len(fn.input_types)
        self.outs = outs if outs != None else [None]*len(fn.output_types)
        self.height = max(len(self.ins), len(self.outs))*20+10
        super().__init__(*args, width=width, height=self.height, **kwargs)
        self.children_refs = self._create_children()
        self.update()
        
    def build_obj(self):
        return Canvas.canvas.create_rectangle(
            self.abs_pos().around(self.width, self.height),
            outline="black",
            fill="#E7B680",
            tags=("draggable", ),
        )

    def _create_children(self) -> list[ObjectReference[MapNode | Label]]:
        children : list[ObjectReference[MapNode | Label]] = []
        for index, _ in enumerate(self.fn.input_types):
            children.append(MapInputNode(self.ref, index, offset=self.abs_pos()).ref)

        for index, _ in enumerate(self.fn.output_types):
            children.append(MapOutputNode(self.ref, index, offset=self.abs_pos()).ref)
            
        children.append(Label(parent_ref=self.ref, name=self.name, offset=self.abs_pos()).ref) 

        return children
    
    def get_value(self):
        in_values = []
        for input in self.ins:
            input_val = input.get_value()
            in_values.append(input_val)
            
        return Node((self.fn.name, self.id), in_values)
    
    def update(self):
        first_in, first_out = None, None
        in_nodes, out_nodes = 0,0
        in_heights, out_heights = 0,0
        max_x_in, max_x_out, label_width = 0,0,0
        end_padding = 7
        end_padding_x = 5
        padding = 5
        text_padding = 5
        
        for child_ref in self.children_refs:
            child = child_ref.obj
            if isinstance(child, MapInputNode):
                first_in = child if first_in == None else first_in
                max_x_in = max(max_x_in, child.width)
                in_heights += child.height
                in_nodes += 1
            elif isinstance(child, MapOutputNode):
                first_out = child if first_out == None else first_out
                max_x_out = max(max_x_out, child.width)
                out_heights += child.height
                out_nodes += 1
            elif isinstance(child, Label):
                label_width = len(child.name)*5.7

        if in_heights > out_heights:
           self.height = in_heights + padding*(in_nodes-1)
        else:
           self.height = out_heights + padding*(out_nodes-1)
        self.height += 2*end_padding
        self.width = max_x_out + max_x_in + label_width + 2*text_padding + 2*end_padding_x

        start_y = -self.height/2 + end_padding
        in_y, out_y = start_y, start_y

        x_size = self.width/2-10
        in_x, out_x = -x_size, x_size

        for child_ref in self.children_refs:
            child = child_ref.obj
            if isinstance(child, MapInputNode):
                in_y += child.height/2
                x = in_x + child.width/2 - text_padding
                child.pos = Point(x, in_y)
                in_y += child.height/2 + padding
            elif isinstance(child, MapOutputNode):
                out_y += child.height/2
                child.pos = Point(out_x, out_y)
                out_y += child.height/2 + padding
            elif isinstance(child, Label):
                x = out_x - first_out.width/2 - label_width/2 - padding
                child.pos = Point(x,0)


        return super().update()
    
    
    def get_all_references(self) -> list[ObjectReference]:
        return super().get_all_references() + self.ins + self.outs
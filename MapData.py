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
            children.append(MapInputNode(self.ref, index, offset=self.abs_pos(), offset_off_parent=Point(0,-self.height/2+5)).ref)

        for index, _ in enumerate(self.fn.output_types):
            children.append(MapOutputNode(self.ref, index, offset=self.abs_pos(), offset_off_parent=Point(0,-self.height/2+5)).ref)
            
        children.append(Label(parent_ref=self.ref, name=self.name, offset=self.abs_pos()).ref) 

        return children
    
    def get_value(self):
        in_values = []
        for input in self.ins:
            input_val = input.get_value()
            in_values.append(input_val)
            
        return Node((self.fn.name, self.id), in_values)
    
    def get_all_references(self) -> list[ObjectReference]:
        return super().get_all_references() + self.ins + self.outs
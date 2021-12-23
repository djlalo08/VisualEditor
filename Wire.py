from __future__ import annotations
from ObjectHierarchy.ObjectReference import ObjectReference
import Utils as u
from Point import Point
from ObjectHierarchy.Object import Object
import Canvas as C
from WireNode import WireNode
from WireSegment import WireSegment
from Tree import Node

class Wire:
    
    def __init__(self, *args, points=[], tags={}, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bound_to_ref: ObjectReference = None #TODO find out which type bound to is
        self.bind_index = 0
        self.children_refs = self.create_wire(points)
        self.update()

    def create_wire(self, points):
        node_refs = []
        for point in points:
            node_refs.append(WireNode(self, pos=point).ref)
        for a, b in u.pairwise(node_refs):
            wire_ref = WireSegment(a, b, parent_ref=self).ref
            a.obj.children_refs.append(wire_ref)
            b.obj.children_refs.append(wire_ref)
        return node_refs
    
    def build_obj(self):
        return C.Canvas.canvas.create_line(Point(0,0).around(1,1))
    
    def get_value(self):
        if self.bound_to_ref == None:
            print("There is a wire in use that has no input")
            return None
        return self.bound_to_ref.obj.get_value() 
    
    def to_front(self):
        for node in self.children_refs:
            C.Canvas.canvas.tag_raise(node.id)
    
    def get_all_references(self) -> list[ObjectReference]:
        return super().get_all_references() + [self.bound_to_ref]

    def update(self):
        for node_ref in self.children_refs:
            node_ref.obj.update()

class InputWire(Wire):
    def __init__(self, *args, index=0, **kwargs) -> None:
        self.index = index
        super().__init__(*args, **kwargs) 
        
    def get_value(self):
        return Node(("in", self.index))

class OutputWire(Wire):
    def __init__(self, *args, index=0, **kwargs) -> None:
        self.index = index
        super().__init__(*args, **kwargs) 

    def get_value(self):
        return Node(("out", self.index), [super().get_value()])

from __future__ import annotations
from ObjectHierarchy.ObjectReference import ObjectReference
import Utils as u
from Point import Point
from ObjectHierarchy.Object import Object
import Canvas as C
from WireNode import WireNode
from WireSegment import WireSegment
from Tree import Node

class Wire(Object):
    
    def __init__(self, *args, points=[], tags={}, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.points = points
        self.bound_to_ref: ObjectReference = None #TODO find out which type bound to is
        self.bind_index = 0
        self.tags = tags
        (self.wire_refs, self.node_refs) = self.create_wire(points)
        self.children_refs = self.node_refs + self.wire_refs

    def create_wire(self, points):
        (wire_refs, node_refs) = ([], [])
        for point in points:
            node_refs.append(WireNode(self.ref, pos=point).ref)
        for a, b in u.pairwise(node_refs):
            wire_ref = WireSegment(a, b, parent_ref=self).ref
            wire_refs.append(wire_ref)
            a.obj.children_refs.append(wire_ref)
            b.obj.children_refs.append(wire_ref)
        for node in node_refs:
            C.Canvas.canvas.tag_raise(node.id) 
        return (wire_refs,node_refs)
    
    def build_obj(self):
        return C.Canvas.canvas.create_line(Point(0,0).around(1,1))
    
    def get_value(self):
        if self.bound_to_ref == None:
            print("There is a wire in use that has no input")
            return None
        return self.bound_to_ref.obj.get_value() 
    
    def to_front(self):
        for wire in self.wire_refs:
            C.Canvas.canvas.tag_raise(wire.id)
        for node in self.node_refs:
            C.Canvas.canvas.tag_raise(node.id)
    
    def get_all_references(self) -> list[ObjectReference]:
        return super().get_all_references() + [self.bound_to_ref]

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

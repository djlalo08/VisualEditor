from __future__ import annotations
import MapData as md
from ObjectHierarchy.ObjectReference import ObjectReference
from ObjectHierarchy.Object import Object
from Point import Point
from ObjectHierarchy.Selectable import Selectable
from Canvas import Canvas
from Tree import Node
from Wire import Wire
from WireNode import WireNode

height = 15
width = 15

class MapNode(Selectable):
    def __init__(self, parent_ref, index, is_input_node=True, **kwargs) -> None:
        super().__init__(parent_ref=parent_ref, constrained_to_parent=True, width=width, height=height, **kwargs)
        self.index = index
        self.value_ref = None
        self.is_input_node = is_input_node
        
    def build_obj(self):
        return Canvas.canvas.create_rectangle(
            self.abs_pos().around(self.width, self.height),
            outline="black",
            fill="white",
            tags=("draggable", "map_node", "selectable"),
        )
        
    def update(self):
        left, top, right, bottom = 0,0,0,0
        for child_ref in self.children_refs:
            child: Object = child_ref.obj
            if isinstance(child, WireNode):
                continue
            c_left, c_top, c_right, c_bottom = child.pos.around(child.width,child.height)
            left = min(c_left, left)
            top = min(c_top, top)
            right = max(c_right, right)
            bottom = max(c_bottom, bottom)
        new_width = (right - left) + height
        new_height = (bottom - top) + width
        if new_width != self.width or new_height != self.height:
            self.width = new_width
            self.height = new_height
            self.parent_ref.obj.update()

        super().update()
        Canvas.canvas.itemconfig(self.id, outline=self.get_outline())
        
    def add_wire_node(self, wire_node: WireNode):
        if self.is_input_node and len(self.children_refs) > 0:
            return 
        self.children_refs.append(wire_node.ref)
        wire_node.pos = Point(0,0)
        wire_node.parent_ref = self.ref
        if self.is_input_node:
            self.value_ref = wire_node.wire
        else:
            wire_node.wire.value_ref = self.ref
            wire_node.bind_index = self.index
        self.update()
        
    @property
    def value(self) -> Node:
        return (self.value_ref.obj.value, self.index)
    
    def get_outline(self):
        return "red" if self.is_selected else "black"
    

class MapInputNode(MapNode):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, is_input_node=True, **kwargs) #type: ignore
        
    @property
    def value(self) -> Node:
        if self.value_ref:
            return Node("inputnode", [self.value_ref.value])
        else:
            raise AttributeError("Node [" + str(self) + "] has no input value")
        

class MapOutputNode(MapNode):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, is_input_node=False, **kwargs) #type: ignore

    @property
    def value(self) -> Node:
        if self.parent_ref:
            return Node("outputnode", [(self.parent_ref.obj.value, self.index)])
        else:
            raise AttributeError("Node [" + str(self) + "] has no parent")
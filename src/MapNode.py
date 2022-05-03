from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from WireNode import WireNode

import MapData as md
from EditorWindow import EditorWindow
from ObjectHierarchy.ObjectReference import ObjectReference
from ObjectHierarchy.Selectable import Selectable
from Point import Point
from Tree import Node
from utils.general import Stream

pad_y = 6
pad_x = 6
height = 15
width = 15

class MapNode(Selectable):
    def __init__(self, parent_ref, index, **kwargs) -> None:
        super().__init__(parent_ref=parent_ref, constrained_to_parent=True, width=pad_x, height=pad_y, **kwargs)
        self.index = index
        self.value_ref = None
        
    def build_obj(self):
        return EditorWindow.canvas.create_rectangle(
            self.abs_pos().around(self.width, self.height),
            outline="black",
            fill="white",
            tags=("draggable", "map_node", "selectable"),
        )
        
    def update(self):
        (new_width, new_height) = self._size
        if new_width != self.width or new_height != self.height:
            self.width = new_width
            self.height = new_height
            self.parent_ref.obj.update()

        super().update()
        EditorWindow.canvas.itemconfig(self.id, outline=self.get_outline())
        
    @property
    def _size(self):
        left, top, right, bottom = 0,0,0,0
        children = Stream(self.children_refs)\
            .map(ObjectReference.get_obj)\
            .iterable

        for child in children:
            c_left, c_top, c_right, c_bottom = child.pos.around(child.width,child.height)
            left = min(c_left, left)
            top = min(c_top, top)
            right = max(c_right, right)
            bottom = max(c_bottom, bottom)
            
        is_occupied = self.is_occupied()
        new_width = (right - left) + (pad_y if is_occupied else height)
        new_height = (bottom - top) + (pad_x if is_occupied else width)
        return (new_width, new_height)
        
    def add_wire_node(self, wire_node: WireNode):
        self.children_refs.append(wire_node.ref)
        wire_node.pos = Point(0,0)
        wire_node.parent_ref = self.ref
        
    @property
    def value(self) -> Node:
        return self.value_ref.obj.value
    
    def get_outline(self):
        return "red" if self.is_selected else "black"
    
    def is_occupied(self) -> bool: 
        if not hasattr(self, 'children_refs'):
            return False
        if not self.children_refs:
            return False
        return True
    
    @property
    def class_name(self) -> str:
        raise NotImplementedError
    
    def __repr__(self) -> str:
        return f"[{self.id}] {self.class_name}: of {{{repr(self.parent_ref)}}}[{self.index}]"
    
def is_map_node(obj) -> bool:
    return isinstance(obj, MapNode)

class MapInputNode(MapNode):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def add_wire_node(self, wire_node: WireNode):
        if len(self.children_refs) > 0:
            return
        super().add_wire_node(wire_node)
        self.value_ref = wire_node.wire
        self.update()

    @property
    def value(self) -> Node:
        if self.value_ref:
            value = self.value_ref.value
            if isinstance(self.value_ref, ObjectReference) and isinstance(self.value_ref.obj, md.MapData):
                value.index = 0
            return value
            
        else:
            raise AttributeError("Node [" + str(self) + "] has no input value")
        
    def value_fn(self) -> Node:
        return self.value
    
    @property
    def class_name(self) -> str:
        return "MapInputNode"
    
def is_input_node(obj):
    return isinstance(obj, MapInputNode)
        

class MapOutputNode(MapNode):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def add_wire_node(self, wire_node: WireNode):
        super().add_wire_node(wire_node)
        wire_node.wire.value_ref = self.ref
        wire_node.bind_index = self.index
        self.update()

    @property
    def value(self) -> Node:
        if self.parent_ref:
            map_val = self.parent_ref.obj.value
            map_val.index = self.index
            return map_val
        else:
            raise AttributeError("Node [" + str(self) + "] has no parent")
        
    @property
    def class_name(self) -> str:
        return "MapOutputNode"

def is_output_node(obj):
    return isinstance(obj, MapOutputNode)

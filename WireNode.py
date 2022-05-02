from __future__ import annotations

from ObjectHierarchy.Selectable import Selectable
import EditorWindow as C
from Tree import Node
import Wire as W

class WireNode(Selectable):
    def __init__(self, wire, width=20, height=20, **kwargs) -> None:
        super().__init__(width=width, height=height, constrained_to_parent=False, **kwargs) 
        self.wire: W.Wire = wire
        
    def build_obj(self):
        return C.EditorWindow.canvas.create_oval(
            self.abs_pos().around(self.width, self.height),
            outline="black",
            fill="#2B9E42",
            tags=("wire", "selectable", "draggable"),
        )
        
    def detach(self):
        print("detaching")

    def update(self):
        super().update()
        self.wire.to_front()
        C.EditorWindow.canvas.itemconfig(self.id, outline=self.get_outline(), fill=self.get_fill())
        
    def get_outline(self):
        return "red" if self.is_selected else "black"
    
    def get_fill(self):
        return "black" if self.parent_ref else "#2B9E42" 
    
    @property
    def value(self) -> Node:
        return self.wire.value
    
    def delete(self):
        if self.parent_ref:
            self.parent_ref.obj.children_refs.remove(self.ref)
        self.parent_ref = None
        
def is_wire_node(obj):
    return isinstance(obj, WireNode)
from __future__ import annotations

from numpy import delete
from ObjectHierarchy.Selectable import Selectable
import Canvas as C
from Tree import Node
import Wire as W

class WireNode(Selectable):
    def __init__(self, wire, width=10, height=10, **kwargs) -> None:
        super().__init__(width=width, height=height, constrained_to_parent=True, **kwargs) 
        self.wire: W.Wire = wire
        
    def build_obj(self):
        return C.Canvas.canvas.create_oval(
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
        C.Canvas.canvas.itemconfig(self.id, outline=self.get_outline(), fill=self.get_fill())
        
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
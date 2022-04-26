from __future__ import annotations
from dataclasses import dataclass
from ObjectHierarchy.Object import Object
from Canvas import Canvas
from ObjectHierarchy.ObjectReference import ObjectReference

@dataclass
class Label(Object):
    parent_ref: ObjectReference = None
    text: str = "map"
    single_point_position : bool = True
    constrained_to_parent : bool = False
    row_name: str = ''
    index: int|None = None
    
    def build_obj(self):
        pos = self.abs_pos().unpack()
        return Canvas.canvas.create_text(pos, text=self.text, fill="black", font=('Helvetica 20 bold'))
    
    def __lt__(self, other):
        return self.index < other.index
    
    def __repr__(self) -> str:
        return f"[{self.id}] Label: {self.text} of {{{repr(self.parent_ref)}}} at {self.row_name}:{self.index}"
        
    def update(self):
        self.width = len(self.text)*5.7*2
        self.height = 20 if self.text else 0
        return super().update()
    
def is_label(obj):
    return isinstance(obj, Label)

from __future__ import annotations
from dataclasses import dataclass
import MapData
from ObjectHierarchy.Object import Object
from Canvas import Canvas
from ObjectHierarchy.ObjectReference import ObjectReference

@dataclass
class Label(Object):
    parent_ref: ObjectReference[MapData.MapData] = None
    name: str = "map"
    single_point_position : bool = True
    constrained_to_parent : bool = False
    
    def build_obj(self):
        pos = self.abs_pos().unpack()
        return Canvas.canvas.create_text(pos, text=self.name, fill="black", font=('Helvetica 10 bold'))
    
def is_label(obj):
    return isinstance(obj, Label)

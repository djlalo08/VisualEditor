from __future__ import annotations
from ObjectHierarchy.Object import Object
import Canvas as C
from ObjectHierarchy.ObjectReference import ObjectReference
from WireNode import WireNode

class WireSegment(Object):
    def __init__(self, a:ObjectReference[WireNode], b:ObjectReference[WireNode], **kwargs) -> None:
        self.a: ObjectReference[WireNode] = a
        self.b: ObjectReference[WireNode] = b
        super().__init__(**kwargs)
        
    def build_obj(self):

        return C.Canvas.canvas.create_line(
            0,0,0,0,
            width = 5,
            fill = '#8AA153',
            tags=("wire", "wire_segment")
        )
        
    def update(self):
        C.Canvas.canvas.coords(self.id, *self.a.obj.abs_pos().unpack(), *self.b.obj.abs_pos().unpack())
        
    def prep_for_save(self):
        super().prep_for_save()

    def prep_from_save_for_use(self, canvas, id_map):
        super().prep_from_save_for_use(canvas, id_map)
    
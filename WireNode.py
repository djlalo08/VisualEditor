from __future__ import annotations
from ObjectHierarchy.Selectable import Selectable
import Canvas as C

class WireNode(Selectable):
    def __init__(self, wire_ref, width=10, height=10, **kwargs) -> None:
        super().__init__(width=width, height=height, constrained_to_parent=True, **kwargs) 
        self.wire_ref = wire_ref
        
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
        self.wire_ref.obj.to_front()
        C.Canvas.canvas.itemconfig(self.id, outline=self.get_outline())
        
    def get_outline(self):
        return "red" if self.is_selected else "black"
    
    def prep_for_save(self):
        super().prep_for_save()

    def prep_from_save_for_use(self, canvas, id_map):
        super().prep_from_save_for_use(canvas, id_map)
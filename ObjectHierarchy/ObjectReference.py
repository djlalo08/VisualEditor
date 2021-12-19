from __future__ import annotations
import Canvas as C
import ObjectHierarchy.Object as O

class ObjectReference:
    def __init__(self, reference: int) -> None:
        self.reference = reference

    def move(self, delta):
        self.get_obj().move(delta)
    
    def abs_pos(self):
        self.get_obj().abs_pos()

    def __invert__(self):
        return self.get_obj().__invert__()
    
    def build_obj(self):
        return self.get_obj().build_obj()
    
    def update(self):
        self.get_obj().update()
            
    def __repr__(self) -> str:
        return self.get_obj().__repr__()
    
    def prep_for_save(self):
        return self.get_obj().prep_for_save()
        
    def prep_from_save_for_use(self, canvas, id_map):
        return self.get_obj().prep_from_save_for_use(canvas, id_map)

    def get_obj(self) -> O.Object:
        return C.Canvas.id_map[self.reference]
from ObjectHierarchy.Object import Object
from Canvas import Canvas

class WireSegment(Object):
    def __init__(self, a, b, **kwargs) -> None:
        self.a = a
        self.b = b
        super().__init__(**kwargs)
        
    def build_obj(self):

        return self.canvas.create_line(
            0,0,0,0,
            width = 5,
            fill = '#8AA153',
            tags=("wire", "wire_segment")
        )
        
    def update(self):
        self.canvas.coords(self.id, *self.a.abs_pos().unpack(), *self.b.abs_pos().unpack())
        
    def prep_for_save(self):
        super().prep_for_save()
        if self.a:
            self.a = self.a.id
        if self.b:
            self.b = self.b.id

    def prep_from_save_for_use(self, canvas, id_map):
        super().prep_from_save_for_use(canvas, id_map)
        if self.a:
            self.a = id_map[self.a]
        if self.b:
            self.b = id_map[self.b]
    
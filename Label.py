from ObjectHierarchy.Object import Object
from Point import Point

class Label(Object):
    def __init__(self, canvas, parent, name, **kwargs) -> None:
        self.name = name
        super().__init__(canvas, parent=parent, single_point_position=True, constrained_to_parent=True, **kwargs)
        
    def build_obj(self):
        pos = self.abs_pos().unpack()
        return self.canvas.create_text(pos, text=self.name, fill="black", font=('Helvetica 10 bold'))
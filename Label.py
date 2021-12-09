from ObjectHierarchy.Object import Object
from Canvas import Canvas

class Label(Object):
    def __init__(self, parent, name, **kwargs) -> None:
        self.name = name
        super().__init__(parent=parent, single_point_position=True, constrained_to_parent=True, **kwargs)
        
    def build_obj(self):
        pos = self.abs_pos().unpack()
        return Canvas.canvas.create_text(pos, text=self.name, fill="black", font=('Helvetica 10 bold'))
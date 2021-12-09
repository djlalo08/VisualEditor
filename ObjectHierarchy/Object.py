from Point import Point
from Canvas import Canvas

class Object:
    
    def __init__( 
            self, 
            pos=Point(0,0), offset=Point(0,0), 
            single_point_position=False,
            parent=None, constrained_to_parent=False, offset_off_parent=Point(0,0),
            children=None, 
            width=0, height=0, 
            **_
    ) -> None:

        self.pos = pos
        self.offset = offset
        self.single_point_position = single_point_position
        self.children = children if children is not None else []
        self.parent = parent
        self.constrained_to_parent = constrained_to_parent
        self.offset_off_parent = offset_off_parent
        self.width = width
        self.height = height
        self.id = self.build_obj()
        Canvas.id_map[self.id] = self

    def move(self, delta):
        if self.parent is not None and self.constrained_to_parent:
            self.parent.move(delta)
        else:
            self.pos += delta
            self.update()
    
    def abs_pos(self):
        return self.pos + self.offset + self.offset_off_parent

    def __INVERT__(self):
        return self.abs_pos()
    
    def build_obj(self):
        raise NotImplementedError("build_obj must overridden but is not")
    
    def update(self):
        newPos = self.abs_pos().around(self.width, self.height)
        if self.single_point_position: 
            newPos = self.abs_pos().unpack()
            
        Canvas.canvas.coords(self.id, newPos)
        for child in self.children:
            child.offset = self.abs_pos()
            child.update()
            
    def __repr__(self) -> str:
        return self.id
    
    def prep_for_save(self):
        if self.parent:
            self.parent = self.parent.id
        if self.children:
            self.children = list(map(lambda c: c.id, self.children))
        
    def prep_from_save_for_use(self, canvas, id_map):
        if self.parent:
            self.parent = id_map[self.parent]
        if self.children:
            self.children = list(map(lambda c_id: id_map[c_id], self.children))
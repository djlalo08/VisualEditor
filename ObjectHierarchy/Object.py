from Point import Point

class Object:
    
    def __init__( 
            self, canvas, 
            pos=Point(0,0), offset=Point(0,0), 
            single_point_position=False,
            parent=None, constrained_to_parent=False, 
            children=None, 
            width=0, height=0, 
            **_
    ) -> None:

        self.canvas = canvas
        self.pos = pos
        self.offset = offset
        self.single_point_position = single_point_position
        self.children = children if children is not None else []
        self.parent = parent
        self.constrained_to_parent = constrained_to_parent
        self.width = width
        self.height = height
        self.id = self.build_obj()

    def move(self, delta):
        if self.parent is not None and self.constrained_to_parent:
            self.parent.move(delta)
        else:
            self.pos += delta
            self.update()
    
    def abs_pos(self):
        return self.pos + self.offset

    def __INVERT__(self):
        return self.abs_pos()
    
    def build_obj(self):
        raise NotImplementedError("build_obj must overridden but is not")
    
    def update(self):
        newPos = self.abs_pos().around(self.width, self.height)
        if self.single_point_position: 
            newPos = self.abs_pos().unpack()
            
        self.canvas.coords(self.id, newPos)
        for child in self.children:
            child.offset = self.abs_pos()
            child.update()
            
    def __repr__(self) -> str:
        return self.id

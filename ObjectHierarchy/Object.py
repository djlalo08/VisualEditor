from __future__ import annotations
from typing_extensions import Self
from Point import Point
import Canvas as C
import ObjectHierarchy.ObjectReference as OR

class Object:
    
    def __init__( 
            self, 
            pos: Point =Point(0,0), 
            offset: Point =Point(0,0), 
            single_point_position: bool = False,
            children_refs: list[OR.ObjectReference]= None, 
            parent_ref: OR.ObjectReference = None, constrained_to_parent: bool = False, offset_off_parent: Point = Point(0,0),
            width: int = 0, height: int =0, 
            **_
    ) -> None:

        self.pos: Point = pos
        self.offset: Point = offset

        self.single_point_position = single_point_position

        self.children_refs : list[OR.ObjectReference] = children_refs if children_refs is not None else []

        self.parent_ref : OR.ObjectReference = parent_ref
        self.constrained_to_parent = constrained_to_parent
        self.offset_off_parent = offset_off_parent

        self.width = width
        self.height = height

        self.id = self.build_obj()
        C.Canvas.id_map[self.id] = self

    def move(self, delta):
        if self.parent_ref is not None and self.constrained_to_parent:
            self.parent_ref.obj.move(delta)
        else:
            self.pos += delta
            self.update()
    
    def abs_pos(self):
        return self.pos + self.offset + self.offset_off_parent
    
    def build_obj(self):
        raise NotImplementedError("build_obj must overridden but is not")
    
    def update(self):
        newPos = self.abs_pos().around(self.width, self.height)
        if self.single_point_position: 
            newPos = self.abs_pos().unpack()
            
        C.Canvas.canvas.coords(self.id, newPos)
        for child_ref in self.children_refs:
            child_ref.obj.offset = self.abs_pos()
            child_ref.obj.update()
            
    def __repr__(self) -> str:
        return self.id
    
    def prep_for_save(self):
        pass
        
    def prep_from_save_for_use(self, canvas, id_map):
        pass
            
    def to_ref(self) -> OR.ObjectReference[Self]:
        return OR.ObjectReference(self.id)

    def __invert__(self) -> OR.ObjectReference[Self]:
        return self.to_ref()
    
    @property
    def ref(self) -> OR.ObjectReference[Self]:
        return self.to_ref()
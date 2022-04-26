from __future__ import annotations
from dataclasses import dataclass, field
from typing_extensions import Self
from Point import Point
import Canvas as C
import ObjectHierarchy.ObjectReference as OR
from Utils import Stream

@dataclass
class Object:
    pos: Point = Point(0,0) 
    offset: Point = Point(0,0) 
    single_point_position: bool = False
    children_refs: list[OR.ObjectReference] = field(default_factory=list)
    parent_ref: OR.ObjectReference = None
    constrained_to_parent: bool = False
    offset_off_parent: Point = Point(0,0)
    width: int = 0
    height: int = 0
    
    def __post_init__(self):
        self.id = self.build_obj()
        C.Canvas.id_map[self.id] = self

    def move(self, delta):
        if self.parent_ref and self.constrained_to_parent:
            self.parent_ref.obj.move(delta)
        else:
            self.pos += delta
            self.update()
    
    def abs_pos(self):
        return self.pos + self.offset + self.offset_off_parent
    
    def build_obj(self):
        raise NotImplementedError("build_obj must overridden but is not")
    
    def get_all_references(self) -> list[OR.ObjectReference]:
        return [self.parent_ref, *self.children_refs]

    def update(self):
        C.Canvas.canvas.tag_raise(self.id)
        newPos = self.abs_pos().around(self.width, self.height)
        if self.single_point_position: 
            newPos = self.abs_pos().unpack()
            
        C.Canvas.canvas.coords(self.id, newPos)
        for child_ref in self.children_refs:
            child_ref.obj.offset = self.abs_pos()
            child_ref.obj.update()
            
            
    def get_all_descendants(self):
        descendants = [self]
        for child_ref in self.children_refs:
            descendants += child_ref.obj.get_all_descendants()
        return descendants
            
    def __repr__(self) -> str:
        return f"[{self.id}] {self.__class__}"

    def to_ref(self) -> OR.ObjectReference[Self]:
        return OR.ObjectReference(self.id)

    def __invert__(self) -> OR.ObjectReference[Self]:
        return self.to_ref()
    
    @property
    def ref(self) -> OR.ObjectReference[Self]:
        return self.to_ref()
    
    @property
    def corners(self) -> list[int]:
        return self.abs_pos().around(self.width, self.height)
        
    def to_front(self) ->None:
        C.Canvas.canvas.tag_raise(self.id)
        for child_ref in self.children_refs:
            child_ref.obj.to_front()
            
    def get_parentest(self) -> Object:
        if not self.parent_ref:
            return self

        return self.parent_ref.obj.get_parentest() 
    
    def delete(self):
        if self.parent_ref:
            self.parent_ref.obj.children_refs.remove(self.ref)

        children = Stream(self.children_refs).map(OR.ObjectReference.get_obj).filter(is_object).to_list()
        for child in children:
           child.delete() 

        C.Canvas.canvas.delete(self.id)
        del C.Canvas.id_map[self.id]
        
def is_object(obj):
    return isinstance(obj, Object)
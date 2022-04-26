from __future__ import annotations
from typing import Generic, TypeVar
import Canvas as C
import ObjectHierarchy.Object as O
from Tree import Node
from misc.dataclassStuff.dataclasses_copy import dataclass

T = TypeVar('T')

@dataclass
class ObjectReference(Generic[T]):
    id : int

    def __repr__(self) -> str:
        return f"#{repr(self.obj)}"

    def get_obj(self) -> T:
        return C.Canvas.id_map[self.id]
    
    def __invert__(self) -> T:
        return self.get_obj()
    
    @property
    def obj(self) -> T:
        return self.get_obj()
    
    @property
    def value(self) -> Node:
        return self.obj.value
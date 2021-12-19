from __future__ import annotations
from typing import Generic, TypeVar
import Canvas as C
import ObjectHierarchy.Object as O

T = TypeVar('T')

class ObjectReference(Generic[T]):
    def __init__(self, id: int) -> None:
        self.id = id

    def get_obj(self) -> T:
        return C.Canvas.id_map[self.id]
    
    def __invert__(self) -> T:
        return self.get_obj()
    
    @property
    def obj(self) -> T:
        return self.get_obj()
    
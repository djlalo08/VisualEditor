from __future__ import annotations

from typing import Generic, TypeVar

import EditorWindow as C
from misc.dataclassStuff.dataclasses_copy import dataclass
from Tree import Node

T = TypeVar('T')

@dataclass
class ObjectReference(Generic[T]):
    id : int

    def __repr__(self) -> str:
        return f"#{repr(self.obj)}"

    def get_obj(self) -> T:
        return C.EditorWindow.id_map[self.id]
    
    def __invert__(self) -> T:
        return self.get_obj()
    
    @property
    def obj(self) -> T:
        return self.get_obj()
    
    @property
    def value(self) -> Node:
        return self.obj.value

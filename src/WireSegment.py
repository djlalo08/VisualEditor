from __future__ import annotations

from typing import TYPE_CHECKING

import EditorWindow as C
from ObjectHierarchy.Object import Object

if TYPE_CHECKING:
    from ObjectHierarchy.ObjectReference import ObjectReference
    from Wire import Wire
    from WireNode import WireNode


class WireSegment(Object):
    def __init__(self, a: ObjectReference[WireNode], b: ObjectReference[WireNode], wire: Wire, **kwargs) -> None:
        self.a: ObjectReference[WireNode] = a
        self.b: ObjectReference[WireNode] = b
        self.wire: Wire = wire
        super().__init__(**kwargs)

    def build_obj(self):
        return C.EditorWindow.canvas.create_line(
            0, 0, 0, 0,
            width=10,
            fill='#8AA153',
            tags=("wire", "wire_segment")
        )

    def update(self):
        C.EditorWindow.canvas.coords(self.id, *self.a.obj.abs_pos().unpack(), *self.b.obj.abs_pos().unpack())

    def get_all_references(self) -> list[ObjectReference]:
        return super().get_all_references() + [self.a, self.b]

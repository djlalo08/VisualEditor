from __future__ import annotations

from dataclasses import dataclass

from ObjectHierarchy.Object import Object
from ObjectHierarchy.ObjectReference import ObjectReference
from EditorWindow import EditorWindow


@dataclass
class Label(Object):
    parent_ref: ObjectReference | None = None
    text: str = "map"
    single_point_position: bool = True
    constrained_to_parent: bool = True
    row_name: str = ''
    index: int | None = None

    def build_obj(self):
        pos = self.abs_pos().unpack()
        return EditorWindow.canvas.create_text(
            pos,
            text=self.text,
            fill="black", 
            font=('Monaco 20 bold'),
            tags=("draggable"))

    def __lt__(self, other):
        return self.index < other.index

    def __repr__(self) -> str:
        return f"[{self.id}] Label: {self.text} of {{{repr(self.parent_ref)}}} at {self.row_name}:{self.index}"

    def update(self):
        self.width = len(self.text)*15
        self.height = 12 if self.text else 0
        return super().update()


def is_label(obj):
    return isinstance(obj, Label)

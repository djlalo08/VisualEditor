from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ObjectHierarchy.ObjectReference import ObjectReference

import EditorWindow as C
import utils.general as u
from Point import Point
from Tree import InputWireNode, Node, OutputWireNode
from WireNode import WireNode
from WireSegment import WireSegment


class Wire:

    def __init__(self, *args, points=[], tags={}, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.value_ref: ObjectReference = None  # TODO find out which type bound to is
        self.bind_index = 0
        self.children_refs = self.create_wire(points)
        self.update()

    def create_wire(self, points):
        node_refs = []
        for point in points:
            node_refs.append(WireNode(self, pos=point).ref)
        for a, b in u.pairwise(node_refs):
            wire_ref = WireSegment(a, b, self).ref
            a.obj.children_refs.append(wire_ref)
            b.obj.children_refs.append(wire_ref)
        return node_refs

    def build_obj(self):
        return C.EditorWindow.canvas.create_line(Point(0, 0).around(1, 1))

    @property
    def value(self) -> Node:
        if self.value_ref == None:
            raise AttributeError("There is a wire in use that has no input")
        return self.value_ref.obj.value

    def to_front(self):
        for node in self.children_refs:
            C.EditorWindow.canvas.tag_raise(node.id)

    def get_all_references(self) -> list[ObjectReference]:
        return super().get_all_references() + [self.value_ref]

    def update(self):
        for node_ref in self.children_refs:
            node_ref.obj.update()


class InputWire(Wire):
    def __init__(self, *args, index=0, **kwargs) -> None:
        self.index = index
        super().__init__(*args, **kwargs)

    @property
    def value(self) -> Node:
        return InputWireNode(self.index)


class OutputWire(Wire):
    def __init__(self, *args, index=0, **kwargs) -> None:
        self.index = index
        super().__init__(*args, **kwargs)

    @property
    def value(self) -> Node:
        return OutputWireNode(self.index, [super().value])

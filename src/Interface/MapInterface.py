from __future__ import annotations

from typing import TYPE_CHECKING

from utils.general import empty_if_null

if TYPE_CHECKING:
    from Interface.InterfaceLabels import InterfaceLabels
    from Interface.MapInterfaceNode import MapInterfaceNode


class MapInterface:

    def __init__(self, name, ins, outs, source=None, labels=None, is_pure=True) -> None:
        self.labels: InterfaceLabels = labels if labels else InterfaceLabels(name)
        self.name: str = name
        self.ins: list[MapInterfaceNode] = empty_if_null(ins)
        self.outs: list[MapInterfaceNode] = empty_if_null(outs)

        self.source: str = source

        self.is_pure: bool = is_pure

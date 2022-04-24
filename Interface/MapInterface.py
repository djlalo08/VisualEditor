from Interface.InterfaceLabels import InterfaceLabels
from Interface.MapInterfaceNode import MapInterfaceNode
from Utils import empty_if_null


class MapInterface:

    def __init__(self, name, ins, outs, source=None, labels=None, is_pure=True) -> None:
        self.labels: InterfaceLabels = labels if labels else InterfaceLabels(name)
        self.name: str = name
        self.ins: list[MapInterfaceNode] = empty_if_null(ins)
        self.outs: list[MapInterfaceNode] = empty_if_null(outs)

        self.source: str = source

        self.is_pure: bool = is_pure
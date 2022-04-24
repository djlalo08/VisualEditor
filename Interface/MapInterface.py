from Interface.InterfaceLabels import InterfaceLabels
from Interface.MapInterfaceNode import MapInterfaceNode
from Utils import empty_if_null


class MapInterface:

    def __init__(self, name, ins, outs, source=None, labels=None, is_pure=True) -> None:
        self.name: str = name
        self.ins: list[MapInterfaceNode] = empty_if_null(ins)
        self.outs: list[MapInterfaceNode] = empty_if_null(outs)

        self.source: str = source

        self.labels: InterfaceLabels = labels
        self.is_pure: bool = is_pure
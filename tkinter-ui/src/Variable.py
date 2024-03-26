from EditorWindow import EditorWindow
from Interface.InterfaceLabels import InterfaceLabels
from Interface.MapInterface import MapInterface
from Interface.MapInterfaceNode import MapInterfaceNode
from MapData import MapData
from Tree import Node, MapDataNode


class SetVariableMap(MapData):
    def __init__(self, name, *args, **kwargs):
        ins = [MapInterfaceNode(name, 'type')]
        labels = InterfaceLabels(name, center=name, in_tops=[''], in_btwns=['', ''], in_bots=[''])
        interface = MapInterface(name, ins, [], '', labels=labels)
        super().__init__(interface, *args, **kwargs)

    @staticmethod
    def background():
        return '#008F00'


class GetVariableMap(MapData):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        outs = [MapInterfaceNode(name, 'type')]
        labels = InterfaceLabels(name, center=name, out_tops=[''], out_btwns=['', ''], out_bots=[''])
        interface = MapInterface(name, [], outs, '', labels=labels)
        super().__init__(interface, *args, **kwargs)

    @staticmethod
    def background():
        return '#008F00'

    @property
    def value(self) -> Node:
        variable_set_map = EditorWindow.vars[self.name]
        return variable_set_map.map_input_nodes[0].value

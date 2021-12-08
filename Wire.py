import Utils as u
from Point import Point
from ObjectHierarchy.Object import Object
from WireNode import WireNode
from WireSegment import WireSegment
from Tree import Node

class Wire(Object):
    
    def __init__(self, *args, points=[], tags={}, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.points = points
        self.bound_to = None
        self.bind_index = 0
        self.tags = tags
        (self.wires, self.nodes) = self.create_wire(points)
        self.children = self.nodes + self.wires

    def create_wire(self, points):
        (wires, nodes) = ([], [])
        for a, b in u.pairwise(points):
            wires.append(WireSegment(self.canvas, self.id_map, a, b, parent=self))

        for index, point in enumerate(points):
            nodes.append(WireNode(self.canvas, self.id_map, self, index, pos=point))
        return (wires,nodes)
    
    def get_wire_segments_for_node(self, node_index):
        a = None if node_index <= 0 else self.wires[node_index-1]
        b = None if node_index >= len(self.wires) else self.wires[node_index]
        return (a, b)
    
    def build_obj(self):
        return self.canvas.create_line(Point(0,0).around(1,1))
    
    def get_value(self):
        if self.bound_to == None:
            print("There is a wire in use that has no input")
            return None
        return self.bound_to.get_value() 
    
    def to_front(self):
        for wire in self.wires:
            self.canvas.tag_raise(wire.id)
        for node in self.nodes:
            self.canvas.tag_raise(node.id)

    def prep_for_save(self):
        super().prep_for_save()
        if self.wires:
            self.wires = list(map(lambda w: w.id, self.wires))
        if self.nodes:
            self.nodes = list(map(lambda n: n.id, self.nodes))
        if self.bound_to:
            self.bound_to = self.bound_to.id

    def prep_from_save_for_use(self, canvas, id_map):
        super().prep_from_save_for_use(canvas, id_map)
        if self.wires:
            self.wires = list(map(lambda w_id: id_map[w_id], self.wires))
        if self.nodes:
            self.nodes= list(map(lambda n_id: id_map[n_id], self.nodes))
        if self.bound_to:
            self.bound_to = id_map[self.bound_to]

class InputWire(Wire):
    def __init__(self, *args, index=0, **kwargs) -> None:
        self.index = index
        super().__init__(*args, **kwargs) 
        
    def get_value(self):
        return Node(("in", self.index))

class OutputWire(Wire):
    def __init__(self, *args, index=0, **kwargs) -> None:
        self.index = index
        super().__init__(*args, **kwargs) 

    def get_value(self):
        return Node(("out", self.index), [super().get_value()])

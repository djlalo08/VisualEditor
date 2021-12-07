import Utils as u
from Point import Point
from Object import Object
from WireNode import WireNode
from WireSegment import WireSegment
from Tree import Node

class Wire(Object):
    
    def __init__(self, canvas, points=[], tags={}, **_) -> None:
        self.canvas = canvas
        self.points = points
        (self.wires, self.nodes) = self.create_wire(points)
        self.id = self.canvas.create_line(Point(0,0).around(1,1))
        self.children = self.nodes + self.wires
        self.bound_to = None
        self.tags = tags

    def create_wire(self, points):
        (wires, nodes) = ([], [])
        for a, b in u.pairwise(points):
            wires.append(WireSegment(self.canvas, a, b))

        for index, point in enumerate(points):
            nodes.append(WireNode(self.canvas, self, index, pos=point))
        return (wires,nodes)
    
    def get_wire_segments_for_node(self, node_index):
        a = None if node_index <= 0 else self.wires[node_index-1]
        b = None if node_index >= len(self.wires) else self.wires[node_index]
        return (a, b)
    
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

class InputWire(Wire):
    def __init__(self, canvas, index=0, **kwargs) -> None:
        self.index = index
        super().__init__(canvas, **kwargs) 
        
    def get_value(self):
        return Node("in-" + str(self.index))

class OutputWire(Wire):
    def __init__(self, canvas, index=0, **kwargs) -> None:
        self.index = index
        super().__init__(canvas, **kwargs) 

    def get_value(self):
        return Node("out-" + str(self.index), [super().get_value()])

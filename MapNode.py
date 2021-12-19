from Point import Point
from ObjectHierarchy.Selectable import Selectable
from Canvas import Canvas

height = 15
width = 15

class MapNode(Selectable):
    def __init__(self, parent, index, is_input_node=True, **kwargs) -> None:
        super().__init__(parent=parent, constrained_to_parent=True, width=width, height=height, **kwargs)
        self.index = index
        self.is_input_node = is_input_node
        
    def build_obj(self):
        return Canvas.canvas.create_rectangle(
            self.abs_pos().around(self.width, self.height),
            outline="black",
            fill="white",
            tags=("draggable", "map_node", "selectable"),
        )
        
    def update(self):
        super().update()
        Canvas.canvas.itemconfig(self.id, outline=self.get_outline())
        
    def add_wire_node(self, wire_node):
        if self.is_input_node and len(self.children) > 0:
            return 
        self.children.append(wire_node)
        wire_node.pos = Point(0,0)
        wire_node.parent = self
        if self.is_input_node:
            self.parent.ins[self.index] = wire_node.wire
        else:
            wire_node.wire.bound_to = self
            wire_node.bind_index = self.index
            self.parent.outs[self.index] = wire_node.wire
        self.update()
        
    def get_value(self):
        parent = self.parent.get_value()
        parent.value = (parent.value, self.index)
        return parent
    
    def get_outline(self):
        return "red" if self.is_selected else "black"

class MapInputNode(MapNode):
    def __init__(self, *args, **kwargs) -> None:
        index = args[1]
        par_width = args[0].width
        pos = Point(-par_width/2+10, index*(height+5)+10)
        super().__init__(*args, is_input_node=True, pos=pos, **kwargs) #type: ignore

class MapOutputNode(MapNode):
    def __init__(self, *args, **kwargs) -> None:
        index = args[1]
        par_width = args[0].width
        pos = Point(par_width/2-10, index*(height+5)+10)
        super().__init__(*args, is_input_node=False, pos=pos, **kwargs) #type: ignore
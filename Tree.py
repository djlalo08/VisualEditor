from typing import Tuple
from typing_extensions import Self
from StringUtils import sanitize


class Node:
    def __init__(self, name=None, index=None, children=[], parent=None, depth=0) -> None:
        self.name = name
        self.index = index
        self.children: list[Node] = children
        self.parent= parent
        self.depth = depth

    def __str__(self) -> str:
        return self.name + "[" + str(self.index) + "]" + self._children_strings
    
    @property
    def _children_strings(self):
        self.update_depths()
        children_strings = []
        for child in self.children:
            child_depth = child.depth if child is not None else 0 
            children_strings.append('\n' + "  "*child_depth + str(child))
        return ''.join(children_strings)
    
    def update_depths(self):
        for child in self.children:
            if child is None: continue
            if isinstance(child, Node):
                child.depth = self.depth + 1
                child.update_depths()
            
    def map_df(self, fn, initial_state):
        state = initial_state
        self.name = fn(self.name, state)
        for child in self.children:
            state = child.map_df(fn, state)
        return state
    
    def get_reduced_children(self, accumulated):
        reduced_children = []
        for child in self.children:
            reduced_child = child.reduce(accumulated)
            reduced_children.append(reduced_child)
        return reduced_children

    def reduce(self, accumulated):
        # raise TypeError("The type of object is wrong: " + self.name)
        pass
            
    @staticmethod
    def child_string(child):
        (name, index) = child
        return name + "[" + str(index) + "]"
        
    
class RootNode(Node):
    def __init__(self, children:list[Node]=[]) -> None:
        super().__init__("root", 0, children, None, 0)
        
    def reduce(self, accumulated):
        self.get_reduced_children(accumulated)
        return accumulated[0]

class InputWireNode(Node):

    def __init__(self, index=None, parent=None, depth=0) -> None:
        super().__init__("in", index, [], parent, depth)

    def reduce(self, accumulated) -> Tuple[str, int]:
        return (self.name, self.index)

class MapDataNode(Node):
    
    def __init__(self, name=None, index=None, obj_id=None, source_file='', children:list[Self|InputWireNode]=[], parent=None, depth=0) -> None:
        super().__init__(name, index, children, parent, depth)
        self.source_file = source_file
        self.obj_id = obj_id
    
    def reduce(self, accumulated):
        name_str = self.name + "_" + str(self.obj_id)
        children = self.get_reduced_children(accumulated)
        arg_list = ", ".join(map(Node.child_string, children)) if children else ""
        (var_decs, var_names) = accumulated
        if name_str not in var_names:
            var_decs.append("Object[] " + sanitize(name_str) + " = " + self.source_file + "(" + arg_list + ");")
            var_names.add(name_str)
        return (name_str, self.index)

class OutputWireNode(Node):

    def __init__(self, index=None, children: list[MapDataNode]=[], parent=None, depth=0) -> None:
        super().__init__("out", index, children, parent, depth)

    def reduce(self, accumulated):
        children = self.get_reduced_children(accumulated)
        assert len(children) == 1
        (child_name, child_index) = children[0]
        accumulated[0].append('out[' + str(self.index) + "] = " + sanitize(child_name) + "[" + str(child_index) + "];")
        return None
        
    
    
'''
a = Node("A") 
b = Node("B") 
c = Node("C")
c.children = [a,b]
d = Node("D")
e = Node("E")
e.children = [c,d]
print(e)
'''
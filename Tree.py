from typing import Tuple


class Node:
    def __init__(self, name=None, index=None, children=[], parent=None, depth=0) -> None:
        self.name = name
        self.index = index
        self.children = children
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
    
    def get_reduced_children(self, vars):
        reduced_children = []
        for child in self.children:
            reduced_child = child.reduce(vars)
            reduced_children.append(reduced_child)
        return reduced_children

    #TODO this is definitely in the wrong place
    def reduce(self, vars):
        if self.name == 'root':
            self.get_reduced_children(vars)
            return vars[0]
        (name, index) = (self.name, self.index)
        if name == 'in':
            children = self.get_reduced_children(vars)
            return (name, index)
        if name == 'out':
            children = self.get_reduced_children(vars)
            assert len(children) == 1
            (child_name, child_index) = children[0]
            vars[0].append('out[' + str(index) + "] = " + child_name + "[" + str(child_index) + "];")
            return None
        if len(name) == 2:
            (fn_name, fn_id) = name
            name_str = fn_name+"_"+str(fn_id)
            children = self.get_reduced_children(vars)
            arg_list = ", ".join(map(Node.child_string, children)) if children is not None else ""
            (var_decs, var_names) = vars
            if name_str not in var_names:
                var_decs.append("Object[] " + name_str+ " = " + fn_name + "(" + arg_list + ");")
                var_names.add(name_str)
            return (name_str, index)
        raise TypeError("The type of object is wrong: " + self.name)
            
    @staticmethod
    def child_string(child):
        (name, index) = child
        return name + "[" + str(index) + "]"
        
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
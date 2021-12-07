class Node:
    def __init__(self, value=None, children=[], parent=None, depth=0) -> None:
        self.value = value
        self.children = children
        self.parent= parent
        self.depth = depth

    def __str__(self) -> str:
        return str(self.value) + self._children_strings()
    
    def _children_strings(self):
        self.update_depths()
        children_strings = []
        for child in self.children:
            children_strings.append('\n' + "  "*child.depth + str(child))
        return ''.join(children_strings)
    
    def update_depths(self):
        for child in self.children:
            child.depth = self.depth + 1
            child.update_depths()
        
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
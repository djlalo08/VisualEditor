'''Everything can only ever have one left,
But things can have multiple rights. I think rights like won't actually get used...'''
from Tree import Node

class DataFlow:
    def __init__(self, bound_to=None, value=None, **kwargs) -> None:
        self.bound_to = bound_to
        self.value = None
        
    def get_value(self, parent=None):
        Node(value=self.value, children=self.left.get_value(), parent=parent)
from functools import reduce
from itertools import tee
from typing import Iterable, List, Type

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def threewise(iterable):
    a, b, c = tee(iterable, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)

class Stream:
    def __init__(self, iterable:Iterable) -> None:
        self.iterable = empty_if_null(iterable)
        
    def map(self, function):
        self.iterable = map(function, self.iterable)
        return self
    
    def filter(self, function):
        self.iterable = filter(function, self.iterable)
        return self
    
    def reduce(self, function):
        return reduce(function, self.iterable)

    def to_list(self) -> List:
        return list(self.iterable)
    
def empty_if_null(list):
    return list if list != None else []
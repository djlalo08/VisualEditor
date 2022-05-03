from inspect import signature

from dataclasses_copy import dataclass

def allow_var_args(func):

    func_params = signature(func).parameters
    def my_func(*args, **kwargs):
        kw_args_we_want = {}
        for param_key in func_params.keys():
            if param_key in kwargs:
                kw_args_we_want[param_key] = kwargs[param_key]
        func(*args, **kw_args_we_want)

    return my_func

def dataclass_var_args(cls):
    cls = dataclass(cls)
    cls.__init__ = allow_var_args(cls.__init__)
    return cls

@dataclass
class Parent:
    offset : int = 0
    pos : int = 0
    x : int = 0
    
@dataclass
class Child(Parent):
    pos: int = 0
    offset : int = 3
    z : int = 5
        
        
p = Parent(1,2)
print(p)
c = Child(1)
print(c)
print(c.x)


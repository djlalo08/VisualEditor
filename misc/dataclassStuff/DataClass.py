from inspect import CO_VARKEYWORDS
from misc.dataclassStuff.inspect_copy import Parameter, getsource, signature

from makefun.main import add_signature_parameters, create_function, with_signature

def kwargs_func(**kwargs):
    print(kwargs)

kw_param = signature(kwargs_func).parameters['kwargs']

def func_with_all(x, y=1, **kwargs):
    print(x,y)
    
func_with_all_sig = signature(func_with_all)

def func(x, y=1):
    print(x, y)
    
func.__code__.co_flags = func.__code__.co_flags | CO_VARKEYWORDS
print(signature(func))

# kw_func_sig = add_signature_parameters(func_sig, last=kw_param)
# kw_func = create_function(func_signature=func_with_all_sig, func_impl=func)

# kw_func(1,2,z=3)
# func_with_all(3,y=5, z=2)
# kw_func(3, y=5, z=2)

# func.__signature__ = 

print(getsource(signature))



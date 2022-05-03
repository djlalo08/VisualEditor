from dataclasses import dataclass
import inspect
from makefun import wraps, with_signature
from makefun.main import add_signature_parameters

# a dummy function
def foo(a, b=1):
    """ foo doc """
    return a + b

# our signature-preserving wrapper
@wraps(foo)
def enhanced_foo(*args, **kwargs):
    print('hello!')
    print('b=%s' % kwargs['b'])  # we can reliably access 'b'
    return foo(*args, **kwargs)

def dataclass_plus(clazz):
    
    clazz = dataclass(clazz)
    '''
    sig = inspect.signature(clazz.__init__)
    new_param = inspect.Parameter("new_param", inspect.Parameter.POSITIONAL_OR_KEYWORD, default=3, annotation=int)
    # new_param = "arg"
    # params = list(sig.parameters)
    # params.append(new_param)
    params = []
    for (_, param) in sig.parameters.items():
        params.append(param)
    params.append(new_param)
    new_sig = sig.replace(parameters=params)
    print(new_sig)
    clazz.__init__.__signature__ = new_sig
    get_sig = inspect.signature(clazz.__init__)
    print(get_sig)
    print(inspect.signature(clazz))
    sig3 = inspect.signature(clazz.__init__)
    print("sig3", sig3)
    '''
    init = clazz.__init__
    star_args = inspect.Parameter("args", inspect.Parameter.VAR_POSITIONAL)
    star_kwargs = inspect.Parameter("kwargs", inspect.Parameter.VAR_KEYWORD)
    params = [star_args, star_kwargs]
    new_init = with_signature(clazz.__init__)
    # @wraps(init)
    # def enhanced_init(self, *args, **kwargs):
        # pass
        # print(inspect.signature(init))
        # return init(self, args[0], args[1])

    clazz.__init__ = new_init
    return clazz

@dataclass_plus
class X:
    x: int
    z: int = 3
    
# a = X(1,2)
# print(a)


def func(*args, **kwargs):
    print (*args)
    print (kwargs['x'])
    
func(1,2,3,4, x=2, y=3) 

def func2(a,b,c=3):
    print(a)

params = inspect.signature(func).parameters
my_params = [params.get('args'), params.get('kwargs')]
for param in params.values():
    print ('args', my_params[0] is param)
    print ('kwargs', my_params[1] is param)

func2(1,2,4)

# func3 = with_signature(inspect.Signature(params.values()))(func2)
func3 = with_signature(inspect.Signature(params.values()))(func2)
# def func3(*args, **kwargs):
    # @with_signature(inspect.Signature(params.values()))


print(inspect.signature(func3))
# func3(1,2,3,4)

@dataclass
class Parent:
        pos : int = 0
        offset : int = 0
        
parent2 = dataclass(Parent)
        
# b= Parent(2,3)
sig = inspect.signature(Parent.__init__)
# sig = add_signature_parameters(sig, last=my_params[0])
sig = add_signature_parameters(sig, last=my_params[1])
Parent.__init__ = with_signature(sig)(Parent.__init__)
p_sig=inspect.signature(Parent.__init__)
print()
print(p_sig)
print(inspect.signature(Parent.__new__))
print(inspect.getsource(Parent))
print(inspect.getsource(parent2))
print()
print('par init', p_sig)
print('par', inspect.signature(Parent))
# b= Parent(2,3,x=4)
# print(b)

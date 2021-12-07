'''
class A:
    def __init__(self, a="a", **_) -> None:
        print("a: " + a)
        
class B(A):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        print("b: " + kwargs["b"])

class C(A):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        print("c: " + kwargs["c"])

class D(B, C):
    def __init__(self) -> None:
        super().__init__(a="da", b="db", c="dc")
        
D()
'''


###############
'''
class A:
    def __init__(self, children=[], **_) -> None:
        self.children = children
        pass
        
class B(A):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.children.append(C("c1"))
        self.children.append(C("c2"))
        self.children.append(C("c3"))

    def __repr__(self) -> str:
        return self.val

class C(A):
    def __init__(self, val, **kwargs) -> None:
        super().__init__(**kwargs)
        self.val = val
        
    def __repr__(self) -> str:
        return self.val

b = B()
c1= b.children[0]
c1.children.append("new item")
print("b children: ", b.children)
print("c1 children ", b.children[0].children)
print("c2 children ", b.children[1].children)
print("c3 children ", b.children[2].children)
'''

'''
class A:
    def __init__(self, children=[]) -> None:
        self.children = children
        
d1 = A().children.append("hi")
d2 = A()
print(d2.children)
'''

#################
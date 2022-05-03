from ObjectHierarchy.Object import Object

class Camera(Object):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    def build_obj(self):
        return -1
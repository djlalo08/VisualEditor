from ObjectHierarchy.Object import Object

class Selectable(Object):
    def __init__(self, canvas, is_selected=False, **kwargs) -> None:
        super().__init__(canvas, **kwargs)
        self.is_selected = is_selected
        
    def select(self):
        self.is_selected = True
        self.update()
    
    def deselect(self):
        self.is_selected = False
        self.update()
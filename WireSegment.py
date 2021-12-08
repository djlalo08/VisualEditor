from ObjectHierarchy.Object import Object

class WireSegment(Object):
    def __init__(self, canvas, id_map, start, end, **kwargs) -> None:
        self.start = start
        self.end = end
        super().__init__(canvas, id_map, **kwargs)
        
    def build_obj(self):
       return self.canvas.create_line(
            self.start.unpack(), self.end.unpack(),
            width = 5,
            fill = 'green',
            tags={"wire",}
        )
        
    def update_start(self, new_start):
        self.start = new_start
        self.update()

    def update_end(self, new_end):
        self.end = new_end
        self.update()
        
    def update(self):
        self.canvas.coords(self.id, self.start.x, self.start.y, self.end.x, self.end.y)
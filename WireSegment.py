
class WireSegment:
    def __init__(self, canvas, start, end) -> None:
        self.canvas = canvas
        self.start = start
        self.end = end
        self.id = self.canvas.create_line(
            start.unpack(), end.unpack(),
            width = 5,
            fill = 'green',
            tags={"wire",}
        )
        self.children = []
        
    def update_start(self, new_start):
        self.start = new_start
        self._update_position()

    def update_end(self, new_end):
        self.end = new_end
        self._update_position()
        
    def _update_position(self):
        self.canvas.coords(self.id, self.start.x, self.start.y, self.end.x, self.end.y)
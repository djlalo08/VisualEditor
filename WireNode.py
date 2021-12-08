from ObjectHierarchy.Selectable import Selectable

class WireNode(Selectable):
    def __init__(self, canvas, id_map, wire, index, width=10, height=10, **kwargs) -> None:
        super().__init__(canvas, id_map, width=width, height=height, constrained_to_parent=True, **kwargs) 
        self.index = index
        self.wire = wire
        
    def build_obj(self):
        return self.canvas.create_oval(
            self.abs_pos().around(self.width, self.height),
            outline="black",
            fill="#2B9E42",
            tags=("wire", "selectable", "draggable"),
        )
        
    def detach(self):
        print("detaching")

    def update(self):
        super().update()
        self._update_wire_segments()
        self.wire.to_front()
        self.canvas.itemconfig(self.id, outline=self.get_outline())

    def _update_wire_segments(self):
        (a, b) = self.wire.get_wire_segments_for_node(self.index)

        a != None and a.update_end(self.abs_pos())
        b != None and b.update_start(self.abs_pos())
        
    def get_outline(self):
        return "red" if self.is_selected else "black"
    
    def prep_for_save(self):
        super().prep_for_save()
        if self.wire:
            self.wire = self.wire.id

    def prep_from_save_for_use(self, canvas, id_map):
        super().prep_from_save_for_use(canvas, id_map)
        if self.wire:
            self.wire = id_map[self.wire]
from ObjectHierarchy.Selectable import Selectable

class WireNode(Selectable):
    def __init__(self, canvas, id_map, wire, width=10, height=10, **kwargs) -> None:
        super().__init__(canvas, id_map, width=width, height=height, constrained_to_parent=True, **kwargs) 
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
        self.wire.to_front()
        self.canvas.itemconfig(self.id, outline=self.get_outline())
        
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
import tkinter as tk
from MapData import *
from MapModal import MapModal
from Wire import Wire, InputWire, OutputWire
from Point import *

'''
#TODO clean up
    - Tags should be nicer and maybe classes (Selectable, Object, etc) should include them
    - Wire.py is a bit unruly. Maybe it should be more of a proper Object. 
        Maybe wire is an example of why Movable should be a class -- wire would be an Object but not movable. 
        On second thought, though, wire should be movable when You pan...
    - Make enum for selection modes
    - Data flow is messyish
    
#TODO add writing directly to java files
#TODO add support for calls to other maps (i.e. I made map x, it uses map y, be able to build map y)
#TODO build standard library over java wrappers
#TODO implement proper class typing
#TODO switch to uing strictly typed python
#TODO implement ability to run code inside editor
'''

canvas_width = 600
    
class EditorCanvas(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.root = parent
        self.canvas = tk.Canvas(width=canvas_width, height=400, background="gray")
        self.canvas.pack(fill="both", expand=True)

        self._drag_data = {"pos": Point(0,0), "item": None}
        self.selected = None
        self.mode = "select"
        self.object_id_map = {}
        self.map_count = 0
        self.ins = []
        self.outs = []

        self.add_map(Point(300,220))
        self.add_in_wire()
        self.add_in_wire()
        self.add_out_wire()

        self.canvas.tag_bind("wire", '<ButtonRelease-1>', self.release_node)
        self.canvas.tag_bind("selectable", '<ButtonPress-1>', self.select_item)
        self.canvas.tag_bind("draggable", "<ButtonPress-1>", self.drag_start)
        self.canvas.tag_bind("draggable", "<ButtonRelease-1>", self.drag_stop)
        self.canvas.tag_bind("draggable", "<B1-Motion>", self.drag)

        parent.bind('<KeyPress-c>', self.connect_mode) #c for connect
        parent.bind('<KeyPress-w>', self.add_free_wire) #w for wire
        parent.bind('<KeyPress-i>', self.add_in_wire) #i for in
        parent.bind('<KeyPress-I>', self.remove_in_wire)
        parent.bind('<KeyPress-o>', self.add_out_wire) # o for out
        parent.bind('<KeyPress-O>', self.remove_out_wire)
        parent.bind('<KeyPress-m>', self.add_map_event) #m for map
        parent.bind('<KeyPress-M>', self.open_map_modal) #m for map
        parent.bind('<KeyPress-e>', self.to_ast) #e for evaluate
        parent.bind('<KeyPress-d>', self.detach_wire) #d for detach

    def drag_start(self, event):
        id = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["item"] = self.object_id_map[id]
        self._drag_data["pos"] = Point(event.x, event.y)

    def drag_stop(self, event):
        self._drag_data["item"] = None
        self._drag_data["pos"] = Point(0,0)

    def drag(self, event):
        delta = Point(event.x, event.y) - self._drag_data["pos"]
        self._drag_data["item"].move(delta)
        self._drag_data["pos"] = Point(event.x, event.y)
        
    def detach_wire(self, event):
        try:
            self.selected.detach()
        except AttributeError:
            pass
        
    def release_node(self, event):
        overlap_range = Point(event.x, event.y).around(5,5)
        all_overlapping = self.canvas.find_overlapping(*overlap_range)
        maps = list(filter(lambda x: "map_node" in self.canvas.gettags(x), all_overlapping))
        if not maps:
            return

        map_node = self.object_id_map.get(maps[0])
        map_node.add_wire_node(self._drag_data["item"])
        
    def select_item(self, event):
        oldSelected = self.selected
        id = self.canvas.find_closest(event.x, event.y)[0]
        self.selected = self.object_id_map[id]

        if self.selected == oldSelected:
            self.selected = None
        else:
            self.do_selection_action(self.selected, oldSelected)

        if oldSelected:
            oldSelected.deselect()

    def do_selection_action(self, newSelection, oldSelection):
        match self.mode:
            case "connect":
                newPos = newSelection.abs_pos()
                delta= newPos - oldSelection.abs_pos()
                oldSelection.move(delta)
                self.mode = "select"
            case "select":
                newSelection.select()

    def register_object(self, object):
        self.object_id_map[object.id] = object
        for child in object.children:
            self.register_object(child)
            
    def deregister_object(self, object):
        self.object_id_map[object.id] = None
        for child in object.children:
            self.deregister_object(child)
            
    def add_in_wire(self, event=None):
        i = len(self.ins)
        y = i*30+200
        points = [Point(30, y), Point(80, y), Point(250, y)]
        wire = InputWire(self.canvas, points=points, index=i)
        self.ins += [wire]
        self.register_object(wire)
        
    def remove_in_wire(self, event):
        # TODO
        pass

    def add_out_wire(self, event=None):
        i = len(self.outs)
        y = i*30+200
        points = [Point(canvas_width-30, y), Point(canvas_width-80, y), Point(canvas_width-250, y)]
        wire = OutputWire(self.canvas, points=points, index=i)
        self.outs += [wire]
        self.register_object(wire)

    def remove_out_wire(self, event):
        # TODO
        pass
    
    def add_free_wire(self, event):
        (x,y) = self.canvas.winfo_pointerxy()
        y -= 60
        x -= 5
        wire = Wire(self.canvas, [Point(x, y), Point(x+50, y)])
        self.register_object(wire)
        
    def add_map_event(self, event=None):
        (x,y) = self.canvas.winfo_pointerxy()
        y -= 60
        x -= 5
        self.add_map(Point(x,y))
        
    def add_map(self, pos=Point(200,200), fn_name="fn", ins=["int", "int"], outs=["int", "int"]):
        count = str(self.map_count)
        fn = Function(fn_name, ins, outs)
        map1 = MapData(self.canvas, pos=pos, name="map"+count, fn=fn)
        self.map_count += 1
        self.register_object(map1)
        
    def connect_mode(self, event):
        self.mode = "connect"
        
    def open_map_modal(self, event):
        pos = Point(*self.canvas.winfo_pointerxy())
        MapModal(self, pos)
        
    def to_ast(self, event=None):
        outValues = map(lambda out: out.get_value(), self.outs)
        program = Node("root", list(outValues))
        reduced = program.reduce(([],set()))
        header = '''public static Object[] example(Object[] in){
        Object[] out = new Object[''' + str(len(self.outs)) + '''];'''
        fn_decls = '\n\t'.join(reduced)
        footer = "\treturn out;\n}"
        print(header)
        print('\t' + fn_decls)
        print(footer)
        #TODO: for each of the outs, crawl brackwards until all is resolved
        pass

if __name__ == "__main__":
    root = tk.Tk()
    EditorCanvas(root).pack(fill="both", expand=True)
    root.mainloop()
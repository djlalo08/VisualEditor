import tkinter as tk
from MapData import *
from MapModal import MapModal
from SaveModal import SaveModal
from OpenModal import OpenModal
from Camera import Camera
from Wire import Wire, InputWire, OutputWire
from Point import *
import pickle

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
    -Add outs support for saving
#TODO build standard library over java wrappers
#TODO implement proper class typing
#TODO switch to uing strictly typed python
#TODO implement ability to run code inside editor
'''

canvas_width = 600
canvas_height = 400
    
class EditorCanvas(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.root = parent
        self.canvas = tk.Canvas(width=canvas_width, height=canvas_height, background="gray")
        self.canvas.pack(fill="both", expand=True)

        self._drag_data = {"pos": Point(0,0), "item": None}
        self.selected = None
        self.mode = "select"
        self.id_map = {}
        self.map_count = 0
        self.ins = []
        self.outs = []
        self.camera = Camera(self.canvas, self.id_map)

        # self.add_some_stuff()

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
        parent.bind('<KeyPress-s>', self.save_modal)#s for save
        parent.bind('<KeyPress-g>', self.open_modal)#g for get
        
    def add_some_stuff(self):
        self.add_map(Point(300,220))
        self.add_in_wire()
        self.add_in_wire()
        self.add_out_wire()

    def open_modal(self, event):
        # OpenModal(self)
        self.load_file("save")
        
    def load_file(self, name):
        with open('lib/'+name, 'rb') as file:
            num_items = pickle.load(file)
            items = []
            for _ in range(num_items):
                item = pickle.load(file)
                item.canvas = self.canvas
                items.append(item)

            for item in items:
                item.id = item.build_obj()
                self.id_map[item.id] = item
                item.id_map = self.id_map
                print("success. Item id: ", item.id)

            out_ids = pickle.load(file)
            self.outs = list(map(lambda o_id: self.id_map[o_id], out_ids))

            for item in items:
                item.prep_from_save_for_use(self.canvas, self.id_map) 
        
    def save_modal(self, event):
        # SaveModal(self)
        self.save_as("save")

    def save_as(self, name):
        with open('lib/'+name, 'wb') as file:
            pickle.dump(len(self.id_map), file)
            for key, value in self.id_map.items():
                value.prep_for_save()
            for key in self.id_map:
                obj = self.id_map.get(key)
                pickle.dump(obj, file)

            o_ids = list(map(lambda o: o.id, self.outs))
            pickle.dump(o_ids, file)

            for key, value in self.id_map.items():
                value.prep_from_save_for_use(self.canvas, self.id_map)


    def drag_start(self, event):
        id = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["item"] = self.id_map[id]
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

        map_node = self.id_map.get(maps[0])
        map_node.add_wire_node(self._drag_data["item"])
        
    def select_item(self, event):
        oldSelected = self.selected
        id = self.canvas.find_closest(event.x, event.y)[0]
        self.selected = self.id_map[id]

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
        self.id_map[object.id] = object
        for child in object.children:
            self.register_object(child)
            
    def deregister_object(self, object):
        self.id_map[object.id] = None
        for child in object.children:
            self.deregister_object(child)
            
    def add_in_wire(self, event=None):
        i = len(self.ins)
        y = i*30+200
        points = [Point(30, y), Point(80, y), Point(250, y)]
        wire = InputWire(self.canvas, self.id_map, points=points, index=i)
        self.ins += [wire]
        self.register_object(wire)
        self.camera.children.append(wire)
        
    def remove_in_wire(self, event):
        # TODO
        pass

    def add_out_wire(self, event=None):
        i = len(self.outs)
        y = i*30+200
        points = [Point(canvas_width-30, y), Point(canvas_width-80, y), Point(canvas_width-250, y)]
        wire = OutputWire(self.canvas, self.id_map, points=points, index=i)
        self.outs += [wire]
        self.register_object(wire)
        self.camera.children.append(wire)

    def remove_out_wire(self, event):
        # TODO
        pass
    
    def add_free_wire(self, event):
        (x,y) = self.canvas.winfo_pointerxy()
        y -= 60
        x -= 5
        wire = Wire(self.canvas, [Point(x, y), Point(x+50, y)])
        self.register_object(wire)
        self.camera.children.append(wire)
        
    def add_map_event(self, event=None):
        (x,y) = self.canvas.winfo_pointerxy()
        y -= 60
        x -= 5
        self.add_map(Point(x,y))
        
    def add_map(self, pos=Point(200,200), fn_name="map", ins=["int", "int"], outs=["int", "int"]):
        fn = Function(fn_name, ins, outs)
        map = MapData(self.canvas, self.id_map, pos=pos, name=fn_name, fn=fn)
        self.register_object(map)
        self.camera.children.append(map)
        
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
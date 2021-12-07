import tkinter as tk
from MapData import *
from Wire import Wire, InputWire, OutputWire
from Point import *

'''
#TODO clean up
    - Tags should be nicer and maybe classes (Selectable, Object, etc) should include them
    - Wire.py is a bit unruly. Maybe it should be more of a proper Object. 
        Maybe wire is an example of why Movable should be a class -- wire would be an Object but not movable. 
        On second thought, though, wire should be movable when You pan...
    - Make enum for selection modes
    - Data flow is a mess

#TODO more work on code generation
    how it will work:
        1) build bottom-up map -- like bfs, but starting at the bottom
        1.5) Collect all ins to be able to build method
        2) Do bottom-up map on tree, for each element You come across -- check if it has been added to state. If not, make a new var for it. Make it a 3-tuple: ('name', #, 'var_name')
        3) Do a df-reduce on the map -- wires are replaced with their var names, maps take their children (all var names now) and replace selves with a line of text: 
            If a var has already been bound, rather than writing x =x, just delete it
            Keep track of all bindings
            Note that all ins are considered to already be bound (they are fn args)
            e.g. 
            ('out', 0, 'out0')
                ('fn', 1, 0)
                  ('in', 0)
                  ('in', 1)

                |       |       |
                V       V       V

            ('out', 0)
                ('fn', 1, 0)
                  in || 0
                  in || 1

                |       |       |
                V       V       V

            ('out', 0)
                fn1 = || 0

            vars = { fn1 = fn(in[0], in[1])}

                |       |       |
                V       V       V

            out[0] = fn1[0]
            
            vars = { fn1 = fn(in[0], in[1])}

            ex2:
            ('out', 0)
              ('fn', 23, 0)
                ('fn', 1, 0)
                  ('in', 0)
                  ('in', 1)
                ('fn', 1, 0)
                  ('in', 0)
                  ('in', 1)

                |       |       |
                V       V       V

            ('out', 0)
              ('fn', 23, 0)
                ('fn', 1, 0)
                  in || 0
                  in || 1
                ('fn', 1, 0)
                  ('in', 0)
                  ('in', 1)

                |       |       |
                V       V       V

            ('out', 0)
              ('fn', 23, 0)
                fn1 || 0
                ('fn', 1, 0)
                  ('in', 0)
                  ('in', 1)
                  
            vars = { fn1 = fn(in[0], in[1])}

                |       |       |
                V       V       V

        This step happens the way it does because next thing we look at is ('fn',1)
        and that value is already in our table, so we just replace it with the var name

            ('out', 0)
              ('fn', 23, 0)
                fn1 || 0
                fn1 || 0

            vars = { fn1 = fn(in0, in1)}

                |       |       |
                V       V       V

            ('out', 0)
              fn23 || 0

            vars = { 
                fn1 = fn(in[0], in[1])
                fn23 = fn(fn1[0], fn1[0])
            }

                |       |       |
                V       V       V

            
            out[0] = fn23[0]

            vars = { 
                fn1 = fn(in[0], in[1])
                fn23 = fn(fn1[0], fn1[0])
            }
        
        ex 3:
        ('out', 0)
          ('fn', 1, 0)
            ('in', 0)
            ('in', 1)
        ('out', 1)
          ('fn', 1, 1)
            ('in', 0)
            ('in', 1)

                |       |       |
                V       V       V

        ('out', 0)
          ('fn', 1, 0)
            in || 0
            in || 1
        ('out', 1)
          ('fn', 1, 1)
            ('in', 0)
            ('in', 1)

                |       |       |
                V       V       V

        ('out', 0)
            fn1 || 0
        ('out', 1)
          ('fn', 1, 1)
            ('in', 0)
            ('in', 1)
              
        vars = { fn1=fn(in[0], in[1])}      

                |       |       |
                V       V       V

        out[0] = fn1[0]
        ('out', 1)
          ('fn', 1, 1)
            ('in', 0)
            ('in', 1)
              
        vars = { fn1=fn(in[0], in[1])}      

                |       |       |
                V       V       V

        out[0] = fn1[0]
        ('out', 1)
            fn1 || 1
              
        vars = { fn1=fn(in[0], in[1])}      

                |       |       |
                V       V       V

        out[0] = fn1[0]
        out[1] = fn1[1]
              
        vars = { fn1=fn(in[0], in[1]) }      
'''



canvas_width = 600
    
class EditorCanvas(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

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
        
    def add_map(self, pos):
        count = str(self.map_count)
        map1 = MapData(self.canvas, pos=pos, name="map"+count)
        self.map_count += 1
        self.register_object(map1)
        
    def connect_mode(self, event):
        self.mode = "connect"

    @staticmethod
    def bind_variables(value, state):
        if len(value) == 2:
            pass
            
    
    def to_ast(self, event=None):
        outValues = map(lambda out: out.get_value(), self.outs)
        program = Node("root", list(outValues))
        reduced = program.reduce(([],set()))
        header = "public static Object[] example(Object[] in){"
        fn_decls = '\n\t'.join(reduced)
        footer = "\treturn out;\n }"
        print(header)
        print('\t' + fn_decls)
        print(footer)
        #TODO: for each of the outs, crawl brackwards until all is resolved
        pass

    

if __name__ == "__main__":
    root = tk.Tk()
    EditorCanvas(root).pack(fill="both", expand=True)
    root.mainloop()
from Canvas import Canvas
from MapModal import MapModal
from SaveModal import SaveModal
from OpenModal import OpenModal
from Tree import Node
from Wire import Wire, InputWire, OutputWire
from WireNode import WireNode
from WireSegment import WireSegment
from Point import Point

'''
#TODO BUGS
    - Can't save file that has been loaded?
    - When using c-mode to jump a map to a wire, if map is in front of wire, program freaks out

#TODO clean up
    - Tags should be nicer and maybe classes (Selectable, Object, etc) should include them
    - Wire.py is a bit unruly. Maybe it should be more of a proper Object. 
        Maybe wire is an example of why Movable should be a class -- wire would be an Object but not movable. 
        On second thought, though, wire should be movable when You pan...
    - Make enum for selection modes
    - Data flow is messyish
    - Clean up save/load
    
#TODO add writing directly to java files
#TODO need to refactor parents and children in general. In general,
    Objects can have more than one parent and more than one type of child.
    I'm thinking something like parent/child is a list of tuples, where 1st elem is name, second is value(s)
    e.g. parent = [('wire', wire), ('bound-to', bound_to)]
    ^^ This above sounds sort of complicated... there must be a better way
#TODO add support for calls to other maps (i.e. I made map x, it uses map y, be able to build map y)
    -Add outs support for saving
#TODO build standard library over java wrappers
#TODO constants support
#TODO implement proper class typing
    - Make types, including lists, etc
#TODO switch to using strictly typed python
    - This will solve our saving issue: things like children, and parent can be typed as ObjectReference, which hold integers but can use id_map to get the actual referred object.
    - Fix saving to accoun for new objectRef system
    - Switch to dataclass impls for classes to make the code nicer and add more type hints
#TODO implement ability to run code inside editor
#TODO ui/ux leaves A LOT to be desired
    - Should be able to extend nodes in cables
    - I can start adding in some syntactic sugar (custom icons for certain operations)
    - m makes another of most recent map
    - map selection is not a modal, but a dropdown pop-up with type-able filter (eventually, filtered by type of fns too)

'''

    
class Bindings:

    def set_bindings(self):

        # self.add_some_stuff()

        Canvas.canvas.tag_bind("wire", '<ButtonRelease-1>', self.release_node)
        Canvas.canvas.tag_bind("selectable", '<ButtonPress-1>', self.select_item)
        Canvas.canvas.tag_bind("draggable", "<ButtonPress-1>", self.drag_start)
        Canvas.canvas.tag_bind("draggable", "<ButtonRelease-1>", self.drag_stop)
        Canvas.canvas.tag_bind("draggable", "<B1-Motion>", self.drag)
        Canvas.canvas.tag_bind("wire_segment", "<ButtonPress-1>", self.add_wire_node)

        Canvas.root.bind('<KeyPress-c>', self.connect_mode) #c for connect
        Canvas.root.bind('<KeyPress-j>', self.wire_edit_mode) #j for connect
        Canvas.root.bind('<KeyPress-w>', self.add_free_wire) #w for wire
        Canvas.root.bind('<KeyPress-i>', self.add_in_wire) #i for in
        Canvas.root.bind('<KeyPress-I>', self.remove_in_wire)
        Canvas.root.bind('<KeyPress-o>', self.add_out_wire) # o for out
        Canvas.root.bind('<KeyPress-O>', self.remove_out_wire)
        Canvas.root.bind('<KeyPress-m>', self.add_map_event) #m for map
        Canvas.root.bind('<KeyPress-M>', self.open_map_modal) #m for map
        Canvas.root.bind('<KeyPress-e>', self.to_ast) #e for evaluate
        Canvas.root.bind('<KeyPress-d>', self.detach_wire) #d for detach
        Canvas.root.bind('<KeyPress-s>', self.save_modal)#s for save
        Canvas.root.bind('<KeyPress-l>', self.open_modal)#l for load
        
        


    def add_some_stuff(self):
        MapModal.add_map(Point(300,220))
        self.add_in_wire()
        self.add_in_wire()
        self.add_out_wire()

    def open_modal(self, event):
        OpenModal()
        
    def save_modal(self, event):
        SaveModal()

    def drag_start(self, event):
        id = Canvas.canvas.find_closest(event.x, event.y)[0]
        Canvas._drag_data["item"] = Canvas.id_map[id]
        Canvas._drag_data["pos"] = Point(event.x, event.y)

    def drag_stop(self, event):
        Canvas._drag_data["item"] = None
        Canvas._drag_data["pos"] = Point(0,0)

    def drag(self, event):
        delta = Point(event.x, event.y) - Canvas._drag_data["pos"]
        Canvas._drag_data["item"].move(delta)
        Canvas._drag_data["pos"] = Point(event.x, event.y)
        
    def detach_wire(self, event):
        try:
            Canvas.selected.detach()
        except AttributeError:
            pass
        
    def release_node(self, event):
        overlap_range = Point(event.x, event.y).around(5,5)
        all_overlapping = Canvas.canvas.find_overlapping(*overlap_range)
        maps = list(filter(lambda x: "map_node" in Canvas.canvas.gettags(x), all_overlapping))
        if not maps:
            return

        map_node = Canvas.id_map.get(maps[0])
        map_node.add_wire_node(Canvas._drag_data["item"])
        
    def select_item(self, event):
        oldSelected = Canvas.selected
        id = Canvas.canvas.find_closest(event.x, event.y)[0]
        Canvas.selected = Canvas.id_map[id]

        if Canvas.selected == oldSelected:
            Canvas.selected = None
        else:
            self.do_selection_action(Canvas.selected, oldSelected)

        if oldSelected:
            oldSelected.deselect()

    def do_selection_action(self, newSelection, oldSelection):
        if Canvas.mode == "connect":
                newPos = newSelection.abs_pos()
                delta= newPos - oldSelection.abs_pos()
                oldSelection.move(delta)
                Canvas.mode = "select"
        if Canvas.mode == "select":
                newSelection.select()

    def add_in_wire(self, event=None):
        i = len(Canvas.in_refs)
        y = i*30+200
        points = [Point(30, y), Point(80, y), Point(250, y)]
        wire = InputWire(points=points, index=i)
        wire.update()
        Canvas.in_refs += [wire.ref]
        
    def remove_in_wire(self, event):
        # TODO
        pass

    def add_out_wire(self, event=None):
        i = len(Canvas.out_refs)
        y = i*30+200
        points = [Point(Canvas.canvas_width-30, y), Point(Canvas.canvas_width-80, y), Point(Canvas.canvas_width-250, y)]
        wire = OutputWire(points=points, index=i)
        wire.update()
        Canvas.out_refs += [wire.ref]

    def remove_out_wire(self, event):
        # TODO
        pass
    
    def add_free_wire(self, event):
        (x,y) = Canvas.canvas.winfo_pointerxy()
        y -= 60
        x -= 5
        wire = Wire(points=[Point(x, y), Point(x+50, y)])
        wire.update()
        
    def add_map_event(self, event=None):
        (x,y) = Canvas.canvas.winfo_pointerxy()
        y -= 60
        x -= 5
        MapModal.add_map(Point(x,y))
        
    def connect_mode(self, event):
        Canvas.mode = "connect"
        
    def wire_edit_mode(self, event):
        Canvas.mode = "wire_edit"

    def open_map_modal(self, event):
        pos = Point(*Canvas.canvas.winfo_pointerxy())
        MapModal(pos)
        
    def add_wire_node(self, event):
        if Canvas.mode != "wire_edit":
            return
        id = Canvas.canvas.find_closest(event.x, event.y)[0]
        wire_segment = Canvas.id_map[id]
        parent_ref = wire_segment.parent_ref
        node = WireNode(parent_ref, pos=Point(event.x, event.y))
        Canvas.id_map[node.id] = node
        b_ref = wire_segment.b
        new_wiresegment = WireSegment(node, b_ref, parent_ref=parent_ref)
        Canvas.id_map[new_wiresegment.id] = new_wiresegment
        wire_segment.b = node
        b_ref.obj.children_refs.remove(wire_segment.ref)
        b_ref.obj.children_refs.append(new_wiresegment.ref)
        node.children_refs.append(new_wiresegment.ref)
        node.children_refs.append(wire_segment.ref)
        node.update()
        Canvas.canvas.tag_raise(node.id)
        parent_ref.obj.nodes_refs.append(node.ref)
        parent_ref.obj.children_refs.append(node.ref)
        Canvas.mode = "select"
        
    def to_ast(self, event=None):
        outValues = map(lambda out: out.obj.get_value(), Canvas.out_refs)
        program = Node("root", list(outValues))
        reduced = program.reduce(([],set()))
        header = '''public static Object[] example(Object[] in){
        Object[] out = new Object[''' + str(len(Canvas.out_refs)) + '''];'''
        fn_decls = '\n\t'.join(reduced)
        footer = "\treturn out;\n}"
        print(header)
        print('\t' + fn_decls)
        print(footer)

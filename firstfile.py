from Canvas import Canvas
from MapData import *
from MapModal import MapModal
from SaveModal import SaveModal
from OpenModal import OpenModal
from Wire import Wire, InputWire, OutputWire
from WireNode import WireNode
from WireSegment import WireSegment
from Point import *
import pickle

'''
#TODO make canvas and id_map global. This will make everything much easier, including saving
    object registration should take place inside Object class
#TODO clean up
    - Tags should be nicer and maybe classes (Selectable, Object, etc) should include them
    - Wire.py is a bit unruly. Maybe it should be more of a proper Object. 
        Maybe wire is an example of why Movable should be a class -- wire would be an Object but not movable. 
        On second thought, though, wire should be movable when You pan...
    - Make enum for selection modes
    - Data flow is messyish
    - Everything is totally crazy after making save work
    
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
#TODO implement ability to run code inside editor
#TODO ui/ux leaves A LOT to be desired
    - Should be able to extend nodes in cables
    - Boxes should look nicer
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
        self.add_map(Point(300,220))
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
        match Canvas.mode:
            case "connect":
                newPos = newSelection.abs_pos()
                delta= newPos - oldSelection.abs_pos()
                oldSelection.move(delta)
                Canvas.mode = "select"
            case "select":
                newSelection.select()

    def register_object(self, object):
        Canvas.id_map[object.id] = object
        for child in object.children:
            self.register_object(child)
            
    def deregister_object(self, object):
        Canvas.id_map[object.id] = None
        for child in object.children:
            self.deregister_object(child)
            
    def add_in_wire(self, event=None):
        i = len(Canvas.ins)
        y = i*30+200
        points = [Point(30, y), Point(80, y), Point(250, y)]
        wire = InputWire(points=points, index=i)
        wire.update()
        Canvas.ins += [wire]
        self.register_object(wire)
        
    def remove_in_wire(self, event):
        # TODO
        pass

    def add_out_wire(self, event=None):
        i = len(Canvas.outs)
        y = i*30+200
        points = [Point(Canvas.canvas_width-30, y), Point(Canvas.canvas_width-80, y), Point(Canvas.canvas_width-250, y)]
        wire = OutputWire(points=points, index=i)
        wire.update()
        Canvas.outs += [wire]
        self.register_object(wire)

    def remove_out_wire(self, event):
        # TODO
        pass
    
    def add_free_wire(self, event):
        (x,y) = Canvas.canvas.winfo_pointerxy()
        y -= 60
        x -= 5
        wire = Wire(points=[Point(x, y), Point(x+50, y)])
        wire.update()
        self.register_object(wire)
        
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
        parent = wire_segment.parent
        node = WireNode(parent, pos=Point(event.x, event.y))
        Canvas.id_map[node.id] = node
        b = wire_segment.b 
        new_wiresegment = WireSegment(node, b, parent=parent)
        Canvas.id_map[new_wiresegment.id] = new_wiresegment
        wire_segment.b = node
        b.children.remove(wire_segment)
        b.children.append(new_wiresegment)
        node.children.append(new_wiresegment)
        node.children.append(wire_segment)
        node.update()
        Canvas.canvas.tag_raise(node.id)
        parent.nodes.append(node)
        parent.children.append(node)
        Canvas.mode = "select"
        
    def to_ast(self, event=None):
        outValues = map(lambda out: out.get_value(), Canvas.outs)
        program = Node("root", list(outValues))
        reduced = program.reduce(([],set()))
        header = '''public static Object[] example(Object[] in){
        Object[] out = new Object[''' + str(len(Canvas.outs)) + '''];'''
        fn_decls = '\n\t'.join(reduced)
        footer = "\treturn out;\n}"
        print(header)
        print('\t' + fn_decls)
        print(footer)
        #TODO: for each of the outs, crawl brackwards until all is resolved
        pass

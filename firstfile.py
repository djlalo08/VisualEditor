from Canvas import Canvas
from MapData import MapData
from MapModal import MapModal
from MapNode import MapInputNode, MapNode
from SaveModal import SaveModal
from OpenModal import OpenModal
from Tree import Node
from Wire import Wire, InputWire, OutputWire
from WireNode import WireNode
from WireSegment import WireSegment
from Point import Point

'''
#TODO BUGS
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
#TODO build standard library over java wrappers
#TODO constants support
#TODO implement proper class typing
    - Make types, including lists, etc
#TODO switch to using strictly typed python
    - This will solve our saving issue: things like children, and parent can be typed as ObjectReference, which hold integers but can use id_map to get the actual referred object.
    - Switch to dataclass impls for classes to make the code nicer and add more type hints
#TODO implement ability to run code inside editor
#TODO ui/ux leaves A LOT to be desired
    - Should be able to extend nodes in cables
    - I can start adding in some syntactic sugar (custom icons for certain operations)
    - m makes another of most recent map
    - map selection is not a modal, but a dropdown pop-up with type-able filter (eventually, filtered by type of fns too)
    - Make code point from top to bottom, rather than left to right (maybe code direction is a setting?)
#TODO LAMBDAS!!!
    - Need to make fns first class first (i.e. they are valid args)
        Ideas about passing fns. All maps must have all of their ins connected to work (maybe some exceptions for optional args or something like that)
        
    - Make the ui such that all kinds of things can be _inside_ (input) MapNode and MapNode should resize accordingly
#TODO stream (see notes on Monday.com) to which variables can be saved
    - Input wires can be read (like stream) from just a box with their name, output wires can just be saved to (I think this bad style maybe tho)
    - Output to fn can be treated as final result, in which case, there is a visual cue to that
'''

    
class Bindings:

    def set_bindings(self):

        # self.add_some_stuff()

        Canvas.canvas.tag_bind("wire", '<ButtonRelease-1>', self.release_node)
        Canvas.canvas.tag_bind("selectable", '<ButtonPress-1>', self.select_item)
        Canvas.canvas.tag_bind("draggable", "<ButtonPress-1>", self.drag_start)
        Canvas.canvas.tag_bind("map_node", "<ButtonPress-2>", self.expand_node)
        Canvas.canvas.tag_bind("draggable", "<ButtonRelease-1>", self.drag_stop)
        Canvas.canvas.tag_bind("draggable", "<B1-Motion>", self.drag)
        Canvas.canvas.tag_bind("wire_segment", "<ButtonPress-1>", self.add_wire_node)

        Canvas.root.bind('<ButtonPress-2>', self.print_cursor)
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
        
    def print_cursor(self, event):
        print(event.x, event.y)

    def add_some_stuff(self):
        self.modal = MapModal.add_map(Point(300,220))
        self.add_in_wire()
        self.add_in_wire()
        self.add_out_wire()

    def open_modal(self, event):
        self.modal = OpenModal()
        
    def save_modal(self, event):
        self.modal = SaveModal()

    def drag_start(self, event):
        id = Canvas.canvas.find_closest(event.x, event.y)[0]
        Canvas._drag_data["item"] = Canvas.id_map[id]
        Canvas._drag_data["pos"] = Point(event.x, event.y)

    def drag_stop(self, event):
        self.drag_map_out_of_node(event)

        Canvas._drag_data["item"] = None
        Canvas._drag_data["pos"] = Point(0,0)

    def drag(self, event):
        delta = Point(event.x, event.y) - Canvas._drag_data["pos"]
        Canvas._drag_data["item"].move(delta)
        Canvas._drag_data["pos"] = Point(event.x, event.y)
        
        self.drag_map_into_node(event)
        
    def drag_map_out_of_node(self, event):
        data_map = Canvas._drag_data["item"]
        if not isinstance(data_map, MapData):
            return False
        
        parent_map_ref = data_map.parent_ref
        if parent_map_ref is None:
            return False
        

        inside_parent = Canvas.canvas.find_enclosed(*parent_map_ref.obj.corners)
        is_inside_parent = False
        for item_id in inside_parent:
            item = Canvas.id_map[item_id]
            if item == data_map:
                is_inside_parent = True 
                break 

        if is_inside_parent:
            return False

        parent_map_ref.obj.children_refs.remove(data_map.ref)
        data_map.parent_ref = None
        data_map.pos = data_map.abs_pos()
        data_map.offset = Point(0,0)
        parent_map_ref.obj.update()
        data_map.update()

    def drag_map_into_node(self, event):
        data_map = Canvas._drag_data["item"]
        if not isinstance(data_map, MapData):
            return
        nearby_ids = Canvas.canvas.find_enclosed(*data_map.corners)
        overlappers = map(lambda id: Canvas.id_map[id], nearby_ids)
        overlapping_in_nodes = list(filter(lambda obj: isinstance(obj, MapInputNode), overlappers))
        map_descs = data_map.get_all_descendants()
        for descendant in map_descs:
            if descendant in overlapping_in_nodes:
                overlapping_in_nodes.remove(descendant)
                
        for node in overlapping_in_nodes:
            node_descendants = node.get_all_descendants()
            if data_map in node_descendants:
                overlapping_in_nodes.remove(node)

        if len(overlapping_in_nodes) == 0:
            return
        node = overlapping_in_nodes[0]
        data_map.parent_ref = node.ref
        data_map.pos = Point(0,0) 
        data_map.to_front()
        node.children_refs.append(data_map.ref)
        node.update()
        
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
                
    def expand_node(self,event):
        print(event.x, event.y)
        print(Point(1,2))
        nearby_ids = Canvas.canvas.find_closest(event.x, event.y, halo=10)
        overlappers = map(lambda id: Canvas.id_map[id], nearby_ids)
        overlapping_nodes = list(filter(lambda obj: isinstance(obj, MapNode), overlappers))
        if not len(overlapping_nodes) == 0:
            node = overlapping_nodes[0]
            print("abs", node.abs_pos())
            print("offset", node.offset)
            print("offset_off_par", node.offset_off_parent)
            print("pos", node.pos)
        
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
        i = len(Canvas.ins)
        x = i*20+200
        points = [Point(x, 30), Point(x, 80), Point(x, 250)]
        wire = InputWire(points=points, index=i)
        Canvas.ins += [wire]
        
    def remove_in_wire(self, event):
        # TODO
        pass

    def add_out_wire(self, event=None):
        i = len(Canvas.outs)
        x = i*20+200
        points = [Point(x, Canvas.canvas_height-30), Point(x, Canvas.canvas_height-80), Point(x, Canvas.canvas_height-250)]
        wire = OutputWire(points=points, index=i)
        Canvas.outs += [wire]

    def remove_out_wire(self, event):
        # TODO
        pass
    
    def add_free_wire(self, event):
        (x,y) = Canvas.canvas.winfo_pointerxy()
        y -= 60
        x -= 5
        wire = Wire(points=[Point(x, y), Point(x, y+50)])
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
        wire_segment_id = Canvas.canvas.find_closest(event.x, event.y)[0] #TODO update [0] with instead looping over all closest and finding first that is a wire
        selected_wire_segment: WireSegment = Canvas.id_map[wire_segment_id]

        parent_wire = selected_wire_segment.parent_ref

        new_node = WireNode(parent_wire, pos=Point(event.x, event.y))

        selected_segments_old_b_ref = selected_wire_segment.b
        new_wiresegment = WireSegment(a=new_node.ref, b=selected_segments_old_b_ref, parent_ref=parent_wire)

        selected_wire_segment.b = new_node.ref
        selected_segments_old_b_ref.obj.children_refs.remove(selected_wire_segment.ref)
        selected_segments_old_b_ref.obj.children_refs.append(new_wiresegment.ref)

        new_node.children_refs.append(new_wiresegment.ref)
        new_node.children_refs.append(selected_wire_segment.ref)
        new_node.update()

        parent_wire.children_refs.append(new_node.ref)

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

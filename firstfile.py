from Bindings.Nester import Nester
from Bindings.Navigator import NavigateDeeper, NavigateHigher, NavigateLeft, NavigateRight
from Bindings.Selector import Selector
from Bindings.WireAdder import WireAdder
from Canvas import Canvas
from CanvasUtils import cursorxy
from MapData import MapData, is_map_data
from MapModal import MapModal
from MapNode import MapNode, is_input_node, is_map_node
from SaveModal import SaveModal
from OpenModal import OpenModal
from Tree import Node
from Utils import Stream, nott
from WireNode import WireNode
from WireSegment import WireSegment
from Point import Point

'''
CURRENTLY WORKING ON -- NAVIGABILITY:
-Make map modal better
    - Autocomplete, based on available files
    - Don't have to specify file info because the file itself already records that
    - This means that every map needs 2 files (or maybe the file can have 2 parts) -- one that specifies the map metadata, like arguments expected and returned, and one that actually has all of the implementation of the file (which in turn can be compiled and evaluated. In reality, there probably should be a third file, which is the byte-code, since in most cases (like standard lib) we don't need to access the inside of the map itself, but we do want to be able to compile and execute it))
        -Ideas about bin: 
            - Should reference other binaries rather than pasting the entire other binaries in. This way, updating a different project doesn't require updating this project. Also means You can do funky stuff with updating code You've received. 
            - For way down the line, there should be full-compile option which compiles into projects with no references. This would make execution faster and also prevent safety issues
    - Making an interface can be independent from making an actual map. Interfaces can have multiple implementations (this is a pref that can be decided on sidebar). Source files can claim to implement an interface. Interface can be made with no impl but when You try to execute code that depends on it, You get a "not implemented"-type error
    - Autocomplete looks for interfaces. If an interface has only 1 impl, then that one is selected. Otherwise user is prompted to select
           
    - 1. Decide on what bin for saved file looks like
    - 2. Update how saving works to save both the src file and the bin file
    - 3. When loading in a map (using map modal), depend on info from the bin file. Modal should have only the text and do a lookup
    - 4. Make the modal small and nice looking, with no buttons or anything (like code suggest popups)
    - 5. Add Autocomplete

#TODO BUGS
    - When a map is nested inside another map, its parent map gets formatted to look pretty but higher up ancestor maps aren't and so things look dumb
    - When using c-mode to jump a map to a wire, if map is in front of wire, program freaks out
    - If You delete stuff and then save, everything goes crazy next time file is loaded up

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
        - Maps are customizable so that symbols can be determined based on items.
        Every map can have a top, bot, left, and right label
        Every arg (and the ouput) can have a top, bot, left and right label (if x, y are adjacent, then x.right_label == y.left_label)
    - m makes another of most recent map
    - map selection is not a modal, but a dropdown pop-up with type-able filter (eventually, filtered by type of fns too)
    - add lines of code, so that code naturally goes in lines across, and to make things more navigable. This will make things less free form and more pretty and easier to edit
    - add refactor commands, like extract (pulls a box out, equivalent to dragging it), and inline (replaces a wire node with the box that it comes from)
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
        Canvas.canvas.tag_bind("selectable", '<ButtonPress-1>', self.click_item)
        Canvas.canvas.tag_bind("draggable", "<ButtonPress-1>", self.drag_start)
        Canvas.canvas.tag_bind("map_node", "<ButtonPress-2>", self.expand_node)
        Canvas.canvas.tag_bind("draggable", "<ButtonRelease-1>", self.drag_stop)
        Canvas.canvas.tag_bind("draggable", "<B1-Motion>", self.drag)
        Canvas.canvas.tag_bind("wire_segment", "<ButtonPress-1>", self.add_wire_node)

        Canvas.root.bind('<ButtonPress-2>', self.print_cursor)
        Canvas.root.bind('<KeyPress-c>', self.connect_mode)  # c for connect
        Canvas.root.bind('<KeyPress-j>', self.wire_edit_mode)  # j for connect
        Canvas.root.bind('<KeyPress-w>', WireAdder.add_free_wire)  # w for wire
        Canvas.root.bind('<KeyPress-i>', WireAdder.add_in_wire)  # i for in
        Canvas.root.bind('<KeyPress-I>', WireAdder.remove_in_wire)
        Canvas.root.bind('<KeyPress-o>', WireAdder.add_out_wire)  # o for out
        Canvas.root.bind('<KeyPress-O>', WireAdder.remove_out_wire)
        Canvas.root.bind('<KeyPress-Down>', self.move_selection_deeper)
        Canvas.root.bind('<KeyPress-Up>', self.move_selection_higher)
        Canvas.root.bind('<KeyPress-Left>', self.move_selection_left)
        Canvas.root.bind('<KeyPress-Right>', self.move_selection_right)
        Canvas.root.bind('<KeyPress-m>', self.add_map_event)  # m for map
        Canvas.root.bind('<KeyPress-M>', self.open_map_modal)  # m for map
        Canvas.root.bind('<KeyPress-E>', self.to_code)  # e for evaluate
        Canvas.root.bind('<KeyPress-e>', self.eval_mode)  # e for evaluate
        Canvas.root.bind('<KeyPress-d>', self.detach_wire)  # d for detach
        Canvas.root.bind('<KeyPress-s>', self.save_modal)  # s for save
        Canvas.root.bind('<KeyPress-l>', self.open_modal)  # l for load
        Canvas.root.bind('<Command-d>', self.debug)  # d for debug
        Canvas.root.bind('<space>', self.insert)
        Canvas.root.bind('<Shift-space>', self.enclose_selection)
        Canvas.root.bind('<BackSpace>', self.delete)
        Canvas.root.bind('<Command-N>', self.new_file_from_interface)

    def delete(self, event):
        if isinstance(Canvas.selected, MapData):
            Canvas.selected.delete()

    def enclose_selection(self, event):
        selection = Canvas.selected
        if not is_map_data(selection):
            return

        MapModal(selection.abs_pos(), enclose=selection)

    def insert(self, event):
        selection = Canvas.selected
        if not is_input_node(selection):
            return

        MapModal(selection.abs_pos(), insert_into=selection)
        
    def new_file_from_interface(self, event):
        pass

    def move_selection_deeper(self, event):
        NavigateDeeper().move_selection()

    def move_selection_higher(self, event):
        NavigateHigher().move_selection()

    def move_selection_right(self, event):
        NavigateRight().move_selection()

    def move_selection_left(self, event):
        NavigateLeft().move_selection()

    def print_cursor(self, event):
        print(event.x, event.y)

    def add_some_stuff(self):
        self.modal = MapModal.add_map(Point(300, 220))
        self.add_in_wire()
        self.add_in_wire()
        self.add_out_wire()

    def debug(self, event):
        outs = Canvas.outs
        id_map = Canvas.id_map
        print("debug")

    def open_modal(self, event):
        self.modal = OpenModal()

    def save_modal(self, event):
        self.modal = SaveModal()

    def drag_start(self, event):
        id = Canvas.canvas.find_closest(event.x, event.y)[0]
        Canvas._drag_data["item"] = Canvas.id_map[id]
        Canvas._drag_data["pos"] = Point(event.x, event.y)

        if Canvas.mode == "eval":
            program = Node("root", None, [Canvas.id_map[id].value])
            print(program)

    def drag_stop(self, event):
        Nester.drag_map_out_of_node()

        Canvas._drag_data["item"] = None
        Canvas._drag_data["pos"] = Point(0, 0)

    def drag(self, event):
        delta = Point(event.x, event.y) - Canvas._drag_data["pos"]
        Canvas._drag_data["item"].move(delta)
        Canvas._drag_data["pos"] = Point(event.x, event.y)

        Nester.drag_map_into_node(Canvas._drag_data["item"])

    def detach_wire(self, event):
        try:
            Canvas.selected.detach()
        except AttributeError:
            pass

    def release_node(self, event):
        overlap_range = Point(event.x, event.y).around(5, 5)
        all_overlapping_ids = Canvas.canvas.find_overlapping(*overlap_range)
        free_maps = Stream(all_overlapping_ids) \
            .map(Canvas.id_map.get) \
            .filter(is_map_node) \
            .filter(nott(MapNode.is_occupied)) \
            .to_list()
        if not free_maps:
            return

        map_node = free_maps[0]
        map_node.add_wire_node(Canvas._drag_data["item"])

    def expand_node(self, event):
        print(event.x, event.y)
        print(Point(1, 2))
        nearby_ids = Canvas.canvas.find_closest(event.x, event.y, halo=10)
        overlappers = map(lambda id: Canvas.id_map[id], nearby_ids)
        overlapping_nodes = list(
            filter(lambda obj: isinstance(obj, MapNode), overlappers))
        if not len(overlapping_nodes) == 0:
            node = overlapping_nodes[0]
            print("abs", node.abs_pos())
            print("offset", node.offset)
            print("offset_off_par", node.offset_off_parent)
            print("pos", node.pos)

    def click_item(self, event):
        id = Canvas.canvas.find_closest(event.x, event.y)[0]
        Selector().select_item(Canvas.id_map[id])

    def add_map_event(self, event=None):
        (x, y) = cursorxy()
        MapModal.add_map(Point(x, y))

    def connect_mode(self, event):
        Canvas.mode = "connect"

    def eval_mode(self, event):
        Canvas.mode = "eval" if Canvas.mode != "eval" else "select"

    def wire_edit_mode(self, event):
        Canvas.mode = "wire_edit"

    def open_map_modal(self, event):
        pos = Point(*cursorxy())
        MapModal(pos)

    def add_wire_node(self, event):
        if Canvas.mode != "wire_edit":
            return
        # TODO update [0] with instead looping over all closest and finding first that is a wire
        wire_segment_id = Canvas.canvas.find_closest(event.x, event.y)[0]
        selected_wire_segment: WireSegment = Canvas.id_map[wire_segment_id]

        parent_wire = selected_wire_segment.parent_ref

        new_node = WireNode(parent_wire, pos=Point(event.x, event.y))

        selected_segments_old_b_ref = selected_wire_segment.b
        new_wiresegment = WireSegment(
            a=new_node.ref, b=selected_segments_old_b_ref, wire=parent_wire)

        selected_wire_segment.b = new_node.ref
        selected_segments_old_b_ref.obj.children_refs.remove(
            selected_wire_segment.ref)
        selected_segments_old_b_ref.obj.children_refs.append(
            new_wiresegment.ref)

        new_node.children_refs.append(new_wiresegment.ref)
        new_node.children_refs.append(selected_wire_segment.ref)
        new_node.update()

        parent_wire.children_refs.append(new_node.ref)

        Canvas.mode = "select"

    def to_ast(self, event=None):
        outValues = map(lambda out: out.value, Canvas.outs)
        program = Node("root", None, list(outValues))
        print(program)
        print()
        return program

    def to_code(self, event=None):
        program = self.to_ast()
        reduced = program.reduce(([], set()))
        header = '''public static Object[] example(Object[] in){
        Object[] out = new Object[''' + str(len(Canvas.outs)) + '''];'''
        fn_decls = '\n\t'.join(reduced)
        footer = "\treturn out;\n}"
        print(header)
        print('\t' + fn_decls)
        print(footer)

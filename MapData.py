from __future__ import annotations

from Label import Label, is_label
from MapNode import MapInputNode, MapNode, MapOutputNode, is_input_node, is_output_node
from ObjectHierarchy.Selectable import Selectable
from Tree import MapDataNode, Node
from ObjectHierarchy.ObjectReference import ObjectReference
from Canvas import Canvas
from Point import Point
from Utils import Stream
import os

LABEL_HEIGHT = 5
END_PADDING_X = 5
END_PADDING_Y = 5
LABEL_PADDING_Y = 10
PADDING_X = 7

def max_height_and_tot_width(items):
    heights = list(map(lambda item: item.height, items))
    max_y = max(heights + [0])
    tot_width = sum(map(lambda item: item.width, items))
    return max_y, tot_width

class MapData(Selectable):
    def __init__(self, interface, *args, width=100, ins=None, outs=None, source_file='', hide_outs=False, **kwargs) -> None:
        self.interface = interface
        self.name = interface.name
        self.ins : ObjectReference[MapNode] = ins if ins != None else [None]*len(interface.ins)
        self.outs: ObjectReference[MapNode] = outs if outs != None else [None]*len(interface.outs)
        self.source_file: str = source_file
        if not source_file:
            print("Source file is blank")
            for file_name in os.listdir("./lib/bin/"):
                if file_name == self.name+'.exec':
                    self.source_file = file_name
                    print("Source file updated")
        self.hide_outs = hide_outs
        self.width = max(len(self.ins), len(self.outs))*20+10
        super().__init__(*args, width=width, height=self.height, **kwargs)
        self.children_refs = self._create_children()
        self.update()
        
    def build_obj(self):
        return Canvas.canvas.create_rectangle(
            self.abs_pos().around(self.width, self.height),
            outline="black",
            fill="#E7B680",
            tags=("draggable", "selectable"),
        )

    def _create_children(self) -> list[ObjectReference[MapNode | Label]]:
        children : list[ObjectReference[MapNode | Label]] = []
        for index, _ in enumerate(self.ins):
            children.append(MapInputNode(self.ref, index, offset=self.abs_pos()).ref)

        for index, _ in enumerate(self.outs):
            children.append(MapOutputNode(self.ref, index, offset=self.abs_pos()).ref)
            
        children.append(Label(parent_ref=self.ref, name=self.name, offset=self.abs_pos()).ref) 

        return children
    
    @property
    def value(self) -> Node:
        input_values = Stream(self.children_refs)\
            .map(ObjectReference.get_obj)\
            .filter(is_input_node)\
            .map(MapInputNode.value_fn)\
            .to_list()
            
        ref = '#'+self.source_file+'#' if self.source_file else self.name
        return MapDataNode(self.name, None, self.id, ref, list(input_values))
    
    @property
    def map_input_nodes(self):
        return Stream(self.children_refs).map(ObjectReference.get_obj).filter(is_input_node).to_list()

    @property
    def map_output_nodes(self):
        return Stream(self.children_refs).map(ObjectReference.get_obj).filter(is_output_node).to_list()

    @property
    def labels(self):
        return Stream(self.children_refs).map(ObjectReference.get_obj).filter(is_label).to_list()
    
    def update(self):
        self.hide_outs = self.parent_ref != None

        input_nodes = self.map_input_nodes
        output_nodes = self.map_output_nodes
        labels = self.labels

        max_y_in, in_widths = max_height_and_tot_width(input_nodes)
        max_y_out, out_widths = max_height_and_tot_width(output_nodes)
                
        for output_node in output_nodes:
            out_state = 'hidden' if self.hide_outs else 'normal'
            Canvas.canvas.itemconfigure(output_node.id, state=out_state)

        label_width = sum(map(lambda label: len(label.name), labels))*5.7

        if in_widths > out_widths:
           self.width = in_widths + PADDING_X*(len(input_nodes)-1)
        else:
           self.width = out_widths + PADDING_X*(len(output_nodes)-1)

        self.width = max(self.width, label_width)
        self.width += 2*END_PADDING_X

        total_height = END_PADDING_Y + max_y_in
        total_height += LABEL_PADDING_Y + LABEL_HEIGHT + LABEL_PADDING_Y
        if not self.hide_outs:
            total_height += max_y_out + END_PADDING_Y 
        self.height = total_height

        start_x = -self.width/2 + END_PADDING_X
        in_x, out_x = start_x, start_x

        y_size = self.height/2 - END_PADDING_Y - LABEL_PADDING_Y
        in_y, out_y = -y_size, y_size

        for input_node in input_nodes:
            in_x += input_node.width/2
            y = in_y + input_node.height/2 - LABEL_PADDING_Y
            input_node.pos = Point(in_x, y)
            in_x += input_node.width/2 + PADDING_X
                
        for output_node in output_nodes:
            out_x += output_node.width/2
            output_node.pos = Point(out_x, out_y)
            out_x += output_node.width/2 + PADDING_X

        first_out = output_nodes and output_nodes[0]
        first_out_height = first_out.height if first_out != None else 0

        for label in labels:
            y = out_y - first_out_height/2 - LABEL_HEIGHT/2 - LABEL_PADDING_Y
            if self.hide_outs:
                y = self.height/2 -LABEL_HEIGHT/2 - LABEL_PADDING_Y
            label.pos = Point(0,y)

        super().update()
        Canvas.canvas.itemconfig(self.id, outline=self.get_outline())

    
    def get_outline(self):
        return "red" if self.is_selected else "black"
    
    def get_all_references(self) -> list[ObjectReference]:
        return super().get_all_references() + self.ins + self.outs
        
    @property
    def input_nodes(self) -> list[MapInputNode]:
        return Stream(self.children_refs).map(ObjectReference.get_obj).filter(is_input_node).to_list()

def is_map_data(obj):
    return isinstance(obj, MapData)
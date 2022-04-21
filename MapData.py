from __future__ import annotations

from Label import Label
from MapNode import MapInputNode, MapNode, MapOutputNode, is_input_node
from Function import Function
from ObjectHierarchy.Selectable import Selectable
from Tree import MapDataNode, Node
from ObjectHierarchy.ObjectReference import ObjectReference
from Canvas import Canvas
from Point import Point
from Utils import Stream
import os

class MapData(Selectable):
    def __init__(self, *args, width=100, ins=None, outs=None, fn=Function(), name="name", source_file='', hide_outs=False, **kwargs) -> None:
        self.fn = fn
        self.name = name
        self.ins : ObjectReference[MapNode] = ins if ins != None else [None]*len(fn.input_types)
        self.outs = outs if outs != None else [None]*len(fn.output_types)
        self.source_file: str = source_file
        if not source_file:
            print("Source file is blank")
            for file_name in os.listdir("./lib/bin/"):
                if file_name == name+'.exec':
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
        for index, _ in enumerate(self.fn.input_types):
            children.append(MapInputNode(self.ref, index, offset=self.abs_pos()).ref)

        for index, _ in enumerate(self.fn.output_types):
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
            
        name = self.fn.name
        ref = '#'+self.source_file+'#' if self.source_file else name
        return MapDataNode(name, None, self.id, ref, list(input_values))
    
    def update(self):
        self.hide_outs = self.parent_ref != None

        first_in, first_out = None, None
        in_nodes, out_nodes = 0,0
        in_widths, out_widths = 0,0
        max_y_in, max_y_out, label_width = 0,0,0
        label_height = 5
        end_padding_x = 5
        end_padding_y = 5
        label_padding_y = 10
        padding_x = 7
        
        for child_ref in self.children_refs:
            child = child_ref.obj
            if isinstance(child, MapInputNode):
                first_in = child if first_in == None else first_in
                max_y_in = max(max_y_in, child.height)
                in_widths += child.width
                in_nodes += 1
            elif isinstance(child, MapOutputNode):
                first_out = child if first_out == None else first_out
                max_y_out = max(max_y_out, child.height)
                out_widths += child.width
                out_nodes += 1
                out_state = 'hidden' if self.hide_outs else 'normal'
                Canvas.canvas.itemconfigure(child.id, state=out_state)
            elif isinstance(child, Label):
                label_width = len(child.name)*5.7

        if in_widths > out_widths:
           self.width = in_widths + padding_x*(in_nodes-1)
        else:
           self.width = out_widths + padding_x*(out_nodes-1)
        self.width = max(self.width, label_width)
        self.width += 2*end_padding_x
        total_height = 0
        total_height += end_padding_y + max_y_in
        total_height += label_padding_y + label_height + label_padding_y
        if not self.hide_outs:
            total_height += max_y_out + end_padding_y 
        self.height = total_height

        start_x = -self.width/2 + end_padding_x
        in_x, out_x = start_x, start_x

        y_size = self.height/2 - end_padding_y - label_padding_y
        in_y, out_y = -y_size, y_size

        first_out_height = first_out.height if first_out != None else 0

        for child_ref in self.children_refs:
            child = child_ref.obj
            if isinstance(child, MapInputNode):
                in_x += child.width/2
                y = in_y + child.height/2 - label_padding_y
                child.pos = Point(in_x, y)
                in_x += child.width/2 + padding_x
            elif isinstance(child, MapOutputNode):
                out_x += child.width/2
                child.pos = Point(out_x, out_y)
                out_x += child.width/2 + padding_x
            elif isinstance(child, Label):
                y = out_y - first_out_height/2 - label_height/2 - label_padding_y
                if self.hide_outs:
                    y = self.height/2 -label_height/2 - label_padding_y
                child.pos = Point(0,y)


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
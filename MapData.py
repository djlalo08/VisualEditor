from __future__ import annotations

from MapNode import MapInputNode, MapNode, MapOutputNode, is_input_node, is_output_node
from ObjectHierarchy.Selectable import Selectable
from Point import Point
from Tree import MapDataNode, Node
from ObjectHierarchy.ObjectReference import ObjectReference
from Canvas import Canvas
from Utils import Stream, empty_if_null
from bisect import insort
from Label import Label, is_label
import os

LABEL_HEIGHT = 5
END_PADDING_X = 5
END_PADDING_Y = 5
LABEL_PADDING_Y = 10
PADDING_X = 7
PAD_TB = 5
PAD_LR = 5

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
        
    def __repr__(self) -> str:
        return f"[{self.id}] MapData: {self.name}"
    
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
            
        if self.interface and self.interface.labels:
            labels = self.interface.labels.create_labels(self)
            for label in labels:
                children.append(label)
        else:
            children.append(Label(parent_ref=self.ref, text=self.name, offset=self.abs_pos()).ref) 

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
    
    def collect_labels_by_row_name(self):
        labels_by_name = {}
        for label in self.labels:
            if label.index == -1:
                labels_by_name[label.row_name] = label
            else:
                if not label.row_name in labels_by_name:
                    labels_by_name[label.row_name] = []
                insort(labels_by_name[label.row_name], label)

        return labels_by_name
    
    def update(self):
        self.hide_outs = self.parent_ref

        input_nodes = self.map_input_nodes
        output_nodes = self.map_output_nodes
        
        self.max_x = 0
                
        self.x0, self.y0 = PAD_LR, PAD_TB
        self.cursor_x, self.cursor_y = self.x0, self.y0
        labels_by_name = self.collect_labels_by_row_name()
        
        # self.pos_label('top', labels_by_name, update_y=True)
        
        in_tops = labels_by_name.get('in_tops')
        in_btwns = labels_by_name.get('in_btwns')
        in_bots = labels_by_name.get('in_bots')
        self.position_a_row(input_nodes, in_tops, in_btwns, in_bots, self.cursor_y)

        self.cursor_x = self.max_x/2
        self.pos_label('center', labels_by_name, update_y=True)
        self.cursor_x = self.x0
        
        if not self.hide_outs:
            out_tops = labels_by_name.get('out_tops')
            out_btwns = labels_by_name.get('out_btwns')
            out_bots = labels_by_name.get('out_bots')
            self.position_a_row(output_nodes, out_tops, out_btwns, out_bots, self.cursor_y)

        self.height = self.cursor_y
        self.width = self.max_x + PAD_LR
        
        #for now, let's just assume that there is no such thing as 'left' text

        # self.pos_label('center', labels_by_name)

        # self.pos_label('bottom', labels_by_name)
        # self.pos_label('right', labels_by_name)
            
        for output_node in output_nodes:
            out_state = 'hidden' if self.hide_outs else 'normal'
            Canvas.canvas.itemconfigure(output_node.id, state=out_state)

        delta = Point(-self.width/2, -self.height/2)
        for child_ref in self.children_refs:
            child = child_ref.obj
            local_delta = Point(child.width/2, 0)
            child.pos += delta + local_delta
            child.update()

        super().update()
        Canvas.canvas.itemconfig(self.id, outline=self.get_outline())

    def position_a_row(self, nodes, tops, btwns, bots, top_of_row):
        nodes = empty_if_null(nodes)
        tops = empty_if_null(tops)
        btwns = empty_if_null(btwns)
        bots = empty_if_null(bots)

        max_row_height = self.get_max_row_height(nodes, tops, bots)

        midpoint_y = top_of_row + max_row_height/2
        for top_label, left_btwn_label, node, bot_label in zip(tops, btwns, nodes, bots):
            self.cursor_x += PAD_LR
            self.cursor_y = top_of_row

            left_btwn_label.pos = Point(self.cursor_x, midpoint_y)
            if left_btwn_label.width:
                self.cursor_x += left_btwn_label.width + PAD_LR
            
            top_label.pos = Point(self.cursor_x, self.cursor_y)
            if top_label.height:
                self.cursor_y += top_label.height + PAD_TB
            
            node.pos = Point(self.cursor_x, midpoint_y)
            if node.height:
                self.cursor_y += node.height + PAD_TB

            bot_label.pos = Point(self.cursor_x, self.cursor_y) 
            if bot_label.height:
                self.cursor_y += bot_label.height + PAD_TB
                        
            self.cursor_x += max([top_label.width, node.width, bot_label.width])
            
        if btwns:
            last_btwn = btwns[-1]
            last_btwn.pos = Point(self.cursor_x, midpoint_y)
            if last_btwn.width:
                self.cursor_x += last_btwn.width + PAD_LR
            
        self.max_x = max(self.max_x, self.cursor_x)
        self.cursor_y = top_of_row + max_row_height

    def get_max_row_height(self, nodes, tops, bots):
        max_row_height = 0
        for top_label, node, bot_label in zip(tops, nodes, bots):
            self.cursor_y = 0

            if top_label.height:
                self.cursor_y += top_label.height + PAD_TB
            if node.height:
                self.cursor_y += node.height + PAD_TB
            if bot_label.height:
                self.cursor_y += bot_label.height + PAD_TB
            
            max_row_height = max (max_row_height, self.cursor_y)
        return max_row_height

    def pos_label(self, row_name, labels_by_name, update_x=False, update_y=False):
        label = labels_by_name.get(row_name)
        if label:
            label.pos = Point(self.cursor_x, self.cursor_y)
            if update_x:
                self.cursor_x += label.width
            if update_y:
                self.cursor_y += label.height
    
    def get_outline(self):
        return "red" if self.is_selected else "black"
    
    def get_all_references(self) -> list[ObjectReference]:
        return super().get_all_references() + self.ins + self.outs
        
    @property
    def input_nodes(self) -> list[MapInputNode]:
        return Stream(self.children_refs).map(ObjectReference.get_obj).filter(is_input_node).to_list()

def is_map_data(obj):
    return isinstance(obj, MapData)
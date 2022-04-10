from abc import abstractmethod

from numpy import empty
from Canvas import Canvas
from ObjectHierarchy.ObjectReference import ObjectReference
from ObjectHierarchy.Selectable import is_selectable
from Bindings.Selector import Selector
from Utils import Stream, get_obj_index

class Navigator:
    @abstractmethod
    def move_selection(self): 
        raise NotImplemented
    
def extract_selectable(ls):
    return Stream(ls).map(ObjectReference.get_obj).filter(is_selectable).to_list()

def get_siblings(obj):
    return (Canvas.selected 
        and Canvas.selected.parent_ref 
        and Canvas.selected.parent_ref.obj.children_refs)

class NavigateDeeper(Navigator):
    def move_selection(self):
        children_refs = Canvas.selected and Canvas.selected.children_refs
        selectable_children = extract_selectable(children_refs)
        if selectable_children:
            Canvas.selected_index = 0
            Selector().select_item(selectable_children[Canvas.selected_index])
    
class NavigateHigher(Navigator):
    def move_selection(self):
        parent_ref = Canvas.selected and Canvas.selected.parent_ref
        if parent_ref:
            Selector().select_item(parent_ref.obj)
            new_index = get_obj_index(get_siblings(parent_ref.obj), parent_ref)
            if new_index != -1:
                Canvas.selected_index = new_index

class NavigateLeftRight(Navigator):
    def move_selection(self):
        selectable_siblings = extract_selectable(get_siblings(Canvas.selected))
        if selectable_siblings:
            old_selection = Canvas.selected_index
            Canvas.selected_index = self.update_index(selectable_siblings)
            if old_selection != Canvas.selected_index:
                Selector().select_item(selectable_siblings[Canvas.selected_index])
                        
    @abstractmethod
    def update_index(self, selectable_children): 
        raise NotImplemented

class NavigateRight(NavigateLeftRight):
    def update_index(self, selectable_children):
        return max(0, min(Canvas.selected_index+1, len(selectable_children)-2))

class NavigateLeft(NavigateLeftRight):
    def update_index(self, _):
        return max(Canvas.selected_index-1, 0)

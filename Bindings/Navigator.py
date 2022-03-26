from abc import abstractmethod
from Canvas import Canvas
from ObjectHierarchy.ObjectReference import ObjectReference
from ObjectHierarchy.Selectable import Selectable
from Bindings.Selector import Selector


class Navigator:
    def move_selection(self): 
        raise NotImplemented

class NavigateDeeper:
    def move_selection(self):
        if Canvas.selected:
            if Canvas.selected.children_refs:
                children = map(ObjectReference.get_obj, Canvas.selected.children_refs) 
                selectable_children = list(filter(lambda child: isinstance(child, Selectable), children))
                if selectable_children:
                    Canvas.selected_index = 0
                    Selector().select_item(selectable_children[Canvas.selected_index])
    
class NavigateHigher:
    def move_selection(self):
        if Canvas.selected:
            if Canvas.selected.parent_ref:
                Selector().select_item(Canvas.selected.parent_ref.obj)

class NavigateLeftRight(Navigator):
    def move_selection(self):
        if Canvas.selected:
            if Canvas.selected.parent_ref:
                children = map(ObjectReference.get_obj, Canvas.selected.parent_ref.obj.children_refs) 
                selectable_children = list(filter(lambda child: isinstance(child, Selectable), children))
                if selectable_children:
                    old_selection = Canvas.selected_index
                    Canvas.selected_index = self.update_index(selectable_children)
                    if old_selection != Canvas.selected_index:
                        Selector().select_item(selectable_children[Canvas.selected_index])
                        
    @abstractmethod
    def update_index(self, selectable_children): 
        raise NotImplemented

class NavigateRight(NavigateLeftRight):
    def update_index(self, selectable_children):
        return min(Canvas.selected_index+1, len(selectable_children)-1)

class NavigateLeft(NavigateLeftRight):
    def update_index(self, selectable_children):
        return max(Canvas.selected_index-1, 0)

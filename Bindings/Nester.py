from Canvas import Canvas
from MapData import MapData
from MapNode import MapInputNode
from Point import Point

class Nester:

    @staticmethod
    def drag_map_out_of_node():
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

    @staticmethod
    def drag_map_into_node(new_contents):
        if not isinstance(new_contents, MapData):
            return
        
        nearby_ids = Canvas.canvas.find_enclosed(*new_contents.corners)
        overlappers = map(lambda id: Canvas.id_map[id], nearby_ids)
        overlapping_in_nodes = list(filter(lambda obj: isinstance(obj, MapInputNode), overlappers))
        map_descs = new_contents.get_all_descendants()
        for descendant in map_descs:
            if descendant in overlapping_in_nodes:
                overlapping_in_nodes.remove(descendant)
                
        for container_node in overlapping_in_nodes:
            node_descendants = container_node.get_all_descendants()
            if new_contents in node_descendants:
                overlapping_in_nodes.remove(container_node)

        if len(overlapping_in_nodes) == 0:
            return
            
        container_node = overlapping_in_nodes[0]
        new_contents.parent_ref = container_node.ref
        new_contents.pos = Point(0,0) 
        new_contents.to_front()
        container_node.children_refs.append(new_contents.ref)
        container_node.value_ref = new_contents.ref
        container_node.update()
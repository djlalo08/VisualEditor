def index(root):
    id_map = {}
    add_element_to_index(root, id_map)
    return id_map

def add_element_to_index(element, id_map):
    if not element: return

    id_map[element.id] = element

    for child in element.children:
        add_element_to_index(child, id_map)
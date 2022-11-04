free_ids = set()  # stuff will get added to this set whenever an element is deleted
max_id = 0

tag_set = {}


def generate_id():
    global max_id
    new_id = free_ids.pop() if len(free_ids) else max_id + 1

    max_id = max(max_id, new_id)
    return new_id


class Tag:
    def __init__(self, name, props=None, children=None, parent=None):
        self.name = name
        self.id = generate_id()
        self.props = props if props else {}
        self.children = children if children else []
        self.parent = parent
        self._has_run = False

        self.props["id"] = f'{{{self.id}}}'

        global tag_set
        tag_set[self.id] = self

    def __repr__(self):
        return my_str(self)

    def __str__(self):
        return my_str(self)

    def __iter__(self):
        return self

    def __next__(self):
        if self._has_run: raise StopIteration

        self._has_run = True
        return self


def my_str(self, tabs='', show_ids=True):
    if not self: return ''
    if isinstance(self, str): return tabs + self + '\n'

    tabs1 = tabs + '\t'
    props_list = [key + ':' + str(self.props.get(key)) for key in self.props.keys()]
    children = [my_str(x, tabs1) for x in self.children]

    return tabs + self.name \
        + ('_' + str(self.id) if show_ids else '') \
        + ('[' + ', '.join(props_list) + ']' if len(props_list) else '') \
        + '\n' \
        + (''.join(children) if len(children) else '')

# print(Tag(
#     'Map',
#     props={
#         'infix': True,
#         'name': 'Min-Max',
#         'ins': [
#             Tag('div', {'id': 2}),
#             Tag('div', {'id': 3})
#         ],
#         'outs': [
#             Tag('div', {'id': 2}),
#             Tag('div', {'id': 3})
#         ]
#     },
#     children=[Tag('Map', {'className': 'constant', 'name': '2'})]
# ))
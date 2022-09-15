class Tag:
    def __init__(self, name, props=None, children=None):
        self.name = name
        self.props = props if props else {}
        self.children = children if children else []

    def __repr__(self):
        return my_str(self)

    def __str__(self):
        return my_str(self)

    def __iter__(self):
        return self

    def __next__(self):
        return self


def my_str(self, tabs=''):
    if not self: return ''
    if isinstance(self, str): return tabs + self + '\n'

    tabs1 = tabs + '\t'
    props_list = [key + ':' + str(self.props.get(key)) for key in self.props.keys() if key not in ['ins', 'outs']]
    children = [my_str(x, tabs1) for x in self.children]

    return tabs + self.name \
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
from translator.clj_example import clojure_code


def parse(code):
    tokens = code \
        .replace('(', ' ( ') \
        .replace(')', ' ) ') \
        .replace('[', ' [ ') \
        .replace(']', ' ] ') \
        .split()
    current_list = ParentedList()
    for token in tokens:
        if token in ['(', '[']:
            new_list = ParentedList(current_list)
            current_list.ls.append(new_list)
            current_list = new_list
        elif token in [')', ']']:
            current_list = current_list.parent
        else:
            current_list.ls.append(token)
    return current_list


def to_jsx(parsed_lists):
    pass


class Tag:
    def __init__(self, name, props=None, children=None):
        self.name = name
        self.props = props if props else {}
        self.children = children if children else []

    def __str__(self):
        return self.my_str()

    def my_str(self, tabs=''):
        tabs1 = tabs + '\t'
        tabs2 = tabs1 + '\t'
        ins = [x.my_str(tabs2) for x in self.props.get('ins', [])]
        outs = [x.my_str(tabs2) for x in self.props.get('outs', [])]
        props_list = [key + ':' + str(self.props.get(key)) for key in self.props.keys() if key not in ['ins', 'outs']]
        children = [x.my_str(tabs2) for x in self.children]

        return tabs + self.name \
               + ('[' + ', '.join(props_list) + ']' if len(props_list) else []) \
               + '\n' \
               + (tabs1 + 'ins: \n' + ''.join(ins) if len(ins) else '') \
               + (tabs1 + 'outs: \n' + ''.join(outs) if len(outs) else '')\
                + (tabs1 + 'children: \n' + ''.join(children) if len(children) else '')


class ParentedList:
    def __init__(self, parent=None):
        self.ls = []
        self.parent = parent

    def __str__(self):
        res = '('
        res += ','.join(map(str, self.ls))
        return res + ')'

    def __repr__(self):
        res = '('
        res += ','.join(map(repr, self.ls))
        return res + ')'

    def convert(self):
        if not self.ls or len(self.ls): return ""

        match self.ls[0]:
            case 'defn':
                inputs = self.ls[2]

            case 'do-vertical':

                return Tag('Vertical', )


if __name__ == '__main__':
    parse(clojure_code)
    print(Tag(
        'Map',
        props={
            'infix': True,
            'name': 'Min-Max',
            'ins': [
                Tag('div', {'id': 2}),
                Tag('div', {'id': 3})
            ],
            'outs': [
                Tag('div', {'id': 2}),
                Tag('div', {'id': 3})
            ]
        },
        children=[Tag('Map', {'className': 'constant', 'name': '2'})]
    ))
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
    return current_list.ls[0]


def to_jsx(selves, tabs='', my_type=''):
    tabs1 = tabs + '\t'
    result = ''

    match my_type:
        case 'props':
            print(selves)
            for key, value in selves.items():
                result += ' ' + key + '=' + to_jsx(value)
            return result

    for self in selves:
        if not self:
            continue
        if isinstance(self, str):
            result += tabs + self
            continue

        if len(self.children):
            result += tabs + '<' + self.name + to_jsx(self.props, my_type='props') + '>\n' \
                      + to_jsx(self.children, tabs1) + '\n' \
                      + tabs + '</' + self.name + '>\n'
        else:
            result += tabs + '<' + self.name + to_jsx(self.props, my_type='props') + '/>\n'
    return result


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
    tabs2 = tabs1 + '\t'
    ins = [my_str(x, tabs2) for x in self.props.get('ins', [])]
    outs = [my_str(x, tabs2) for x in self.props.get('outs', [])]
    props_list = [key + ':' + str(self.props.get(key)) for key in self.props.keys() if key not in ['ins', 'outs']]
    children = [my_str(x, tabs2) for x in self.children]

    return tabs + self.name \
           + ('[' + ', '.join(props_list) + ']' if len(props_list) else '') \
           + '\n' \
           + (tabs1 + 'ins: \n' + ''.join(ins) if len(ins) else '') \
           + (tabs1 + 'outs: \n' + ''.join(outs) if len(outs) else '') \
           + (tabs1 + 'children: \n' + ''.join(children) if len(children) else '')


class ParentedList:
    def __init__(self, parent=None):
        self.ls = []
        self.parent = parent
        self.current_index = 0

    def __str__(self):
        res = '('
        res += ','.join(map(str, self.ls))
        return res + ')'

    def __repr__(self):
        res = '('
        res += ','.join(map(repr, self.ls))
        return res + ')'

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index >= len(self.ls):
            raise StopIteration

        res = self.ls[self.current_index]
        self.current_index += 1
        return res


def to_tag(self, my_type=''):
    match my_type:
        case 'input':
            return Tag('Map', {'className': 'io',
                               'name': self
                               })

        case 'output':
            return Tag('Map', {'className': 'io',
                               'name': self
                               })

        case 'ins':
            return Tag('div')

    if not isinstance(self, ParentedList):
        return self
    ls = self.ls
    if len(ls) == 1:
        return ls[0]

    match ls[0]:
        case 'defx':
            [_, name, ins, lines, outs] = ls
            ins = Tag('Horizontal', {}, [to_tag(x, 'input') for x in ins])
            lines = Tag('Vertical', {}, [to_tag(x) for x in lines])
            outs = Tag('Horizontal', {}, [to_tag(x, 'output') for x in outs])
            return [ins, lines, outs]
        case 'make-map':
            [_, map_name, ins, outs] = ls
            props = {'name': map_name, 'ins': [to_tag(x, 'ins') for x in ins], 'outs': [to_tag(x, 'outs') for x in outs]}
            return Tag('Map', props)
        case 'outsmap':
            [_, var_name] = ls
            return Tag('div', {'id': var_name})


if __name__ == '__main__':
    parsed = parse(clojure_code)
    print('parsed\n', parsed)

    tagged = to_tag(parsed)
    print('tagged\n', tagged)

    jsx = to_jsx(tagged)
    print('jsx\n', jsx)

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
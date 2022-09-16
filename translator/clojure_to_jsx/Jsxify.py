from translator.clojure_to_jsx.Tagify import str0

all_wires = {}
wires_list = []

def to_jsx(selves):
    jsx = to_jsx_(selves) + '\n'
    wires = '\n'.join(wires_list)
    return jsx + wires
def to_jsx_(selves, tabs='', my_type=''):
    tabs1 = tabs + '\t'
    result = ''

    match my_type:
        case 'props':
            # print(selves)
            for key, value in selves.items():
                result += ' ' + key + '=' + to_jsx_(value)
            return result

    for self in selves:
        if not self:
            continue
        elif isinstance(self, str):
            result += tabs + self
            continue

        elif self.name in ['SetNode', 'GetNode']:
            value = self.props.get('value')
            if self.name == 'SetNode':
                if value in all_wires:
                    raise RuntimeWarning('There is a duplicated output wire')
                all_wires[value] = 0
            if self.name == 'GetNode':
                temp = value
                value = str(value) + '_' + str(all_wires[value])
                all_wires[temp] += 1
                wires_list.append('<Wire start=' + str0(temp) + ' end=' + str0(value) + '/>')
            result += str0(value) if self.props.get('x') else \
                tabs + '<div id=' + str0(value) + '/>\n'

        elif self.name in ['FileInput', 'FileOutput']:
            result += tabs + '<' + self.name + to_jsx_(self.props, my_type='props') + '>' \
                      + '{[' + ','.join(map(to_jsx_, self.children)) + ']}' \
                      + '</' + self.name + '>\n'

        elif len(self.children):
            result += tabs + '<' + self.name + to_jsx_(self.props, my_type='props') + '>\n' \
                      + to_jsx_(self.children, tabs1) \
                      + tabs + '</' + self.name + '>\n'
        else:
            result += tabs + '<' + self.name + to_jsx_(self.props, my_type='props') + '/>\n'
    return result
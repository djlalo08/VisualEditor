from translator.clojure_to_jsx.Tagify import str0


def to_jsx(selves, tabs='', my_type=''):
    tabs1 = tabs + '\t'
    result = ''

    match my_type:
        case 'props':
            # print(selves)
            for key, value in selves.items():
                result += ' ' + key + '=' + to_jsx(value)
            return result

    for self in selves:
        if not self:
            continue
        elif isinstance(self, str):
            result += tabs + self
            continue

        elif self.name in ['FileInput', 'FileOutput']:
            result += tabs + '<' + self.name + to_jsx(self.props, my_type='props') + '>'\
                      + '{[' + ','.join(map(str0, self.children)) + ']}' \
                      + '</' + self.name + '>\n'

        elif len(self.children):
            result += tabs + '<' + self.name + to_jsx(self.props, my_type='props') + '>\n' \
                      + to_jsx(self.children, tabs1) \
                      + tabs + '</' + self.name + '>\n'
        else:
            result += tabs + '<' + self.name + to_jsx(self.props, my_type='props') + '/>\n'
    return result
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
                      + to_jsx(self.children, tabs1) \
                      + tabs + '</' + self.name + '>\n'
        else:
            result += tabs + '<' + self.name + to_jsx(self.props, my_type='props') + '/>\n'
    return result
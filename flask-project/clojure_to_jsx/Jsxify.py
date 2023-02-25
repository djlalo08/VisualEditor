from clojure_to_jsx.Tagify import str0

all_wires = {}
wires_list = []


def to_jsx(selves):
    jsx = _to_jsx(selves) + '\n'
    wires = '\n'.join(wires_list)
    body = jsx + wires
    return header + body + footer


def _to_jsx(selves, tabs=''):
    tabs1 = tabs + '\t'
    result = ''

    print('before')
    for self in selves:
        print('1')
        if not self:
            print('2')
            continue
        elif isinstance(self, str):
            print('3')
            result += tabs + self
            continue

        elif self.name in ['SetNode', 'GetNode']:
            print('4')
            value = self.props.get('value')
            if self.name == 'SetNode':
                if value in all_wires:
                    pass
                    # raise RuntimeWarning('There is a duplicated output wire')
                all_wires[value] = 0
            if self.name == 'GetNode':
                temp = value
                if value in all_wires:
                    value = str(value) + '_' + str(all_wires[value])
                if temp in all_wires:
                    all_wires[temp] += 1
                wires_list.append('<Wire start=' + str0(temp) + ' end=' + str0(value) + '/>')
            result += str0(value) if self.props.get('x') else \
                tabs + '<div id=' + str0(value) + '/>\n'

        elif self.name in ['FileInput', 'FileOutput']:
            print('5')
            result += tabs + f"<{name_and_props(self)}>" \
                      + f"{{[{','.join(map(_to_jsx, self.children))}]}}" \
                      + f"</{self.name}>\n"

        elif len(self.children):
            print('6')
            result += tabs + f"<{name_and_props(self)}>\n" \
                      + _to_jsx(self.children, tabs1) \
                      + tabs + '</' + self.name + '>\n'
        else:
            print('7')
            result += tabs + f"<{self.name}{props_to_jsx(self.props)}/>\n"
    print('result:', result[:30])
    return result


def name_and_props(tag):
    return f"{tag.name}{props_to_jsx(tag.props)}"


def props_to_jsx(props):
    return ''.join([f' {key}={_to_jsx(value)}' for (key, value) in props.items()])


header = '''
import { Xwrapper } from 'react-xarrows';
import FileInput from './FileInput';
import FileOutput from './FileOutput';
import Horizontal from './Horizontal';
import Ins from './Ins';
import Map from './Map';
import Node from './Node';
import Outs from './Outs';
import Root from './Root';
import Vertical from './Vertical';
import Wire from './Wire';

export default function GeneratedApp(){
    return( <Xwrapper>
    
'''

footer = '''
    </Xwrapper>);
}
'''
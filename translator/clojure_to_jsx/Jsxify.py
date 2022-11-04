from translator.clojure_to_jsx.Tagify import str0

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
            result += tabs + f"<{name_and_props(self)}>" \
                        + f"{{[{ ','.join(map(_to_jsx, self.children)) }]}}" \
                        + f"</{self.name}>\n"

        elif len(self.children):
            result += tabs + f"<{name_and_props(self)}>\n" \
                      + _to_jsx(self.children, tabs1) \
                      + tabs + '</' + self.name + '>\n'
        else:
            result += tabs + f"<{self.name}{props_to_jsx(self.props)}/>\n"
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
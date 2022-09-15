from translator.clojure_to_jsx.ParentedList import ParentedList
from translator.clojure_to_jsx.Tag import Tag

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
            props = {'name': map_name}
            ins = Tag('Ins', children=[to_tag(x) for x in ins])
            outs = Tag('Outs', children=[to_tag(x) for x in outs])
            return Tag('Map', props, [ins, outs])
        case 'outsmap':
            [_, var_name] = ls
            return Tag('div', {'id': '"' + var_name + '"'})
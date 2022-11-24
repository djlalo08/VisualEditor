from clojure_to_jsx.ParentedList import ParentedList
from clojure_to_jsx.Tag import Tag


def to_tag(self, my_type=''):
    meta = self.meta if isinstance(self, ParentedList) else {}

    match my_type:
        case 'FileInput':
            children = self.ls if isinstance(self, ParentedList) else [self]
            return Tag('FileInput', meta, [Tag('SetNode', {'value': child, 'x': True}) for child in children])
        case 'FileOutput':
            children = self.ls if isinstance(self, ParentedList) else self
            return Tag('FileOutput', meta, [Tag('GetNode', {'value': child, 'x': True}) for child in children])

    if not isinstance(self, ParentedList):
        return Tag('SetNode', {'value': self})
    ls = self.ls
    if len(ls) == 1:
        return Tag('Map', {'name': str0(ls[0]), **meta})

    match ls[0]:
        case 'defx':
            [_, name, ins, lines, outs] = ls
            ins = Tag('Horizontal', meta, [to_tag(x, 'FileInput') for x in ins])
            lines = Tag('Vertical', meta, [to_tag(x) for x in lines])
            outs = Tag('Horizontal', meta, [to_tag(x, 'FileOutput') for x in outs])
            return Tag('Root', meta, [ins, lines, outs])
        case 'make-map':
            [_, map_name, ins, outs] = ls
            props = {'name': str0(map_name)}
            ins = Tag('Ins', meta, [to_tag(x) for x in ins])
            outs = Tag('Outs', meta, [to_tag(x) for x in outs])
            return Tag('Map', props | meta, [ins, outs])
        case 'outsmap':
            [_, var_name] = ls
            return Tag('GetNode', {'value': var_name})

def str0(obj):
    return '"' + str(obj) + '"'
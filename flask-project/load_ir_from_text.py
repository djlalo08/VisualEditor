from clojure_to_jsx.Tag import Tag

def get_indent_level(line: str):
    full_line = line.rstrip()
    unindented = line.lstrip()
    return (len(full_line) - len(unindented))//4

def associate(parent, child):
    child.parent = parent
    parent.children.append(child)

def parse_line(line: str):
    line = line.strip()
    if not line.count('['): return line, {}

    name, props_str = line.split('[', 1)
    props_str = props_str[:-1]

    props = {}
    for pair in props_str.split(','):
        key, value = pair.strip().split(':', 1)
        props[key.strip()] = value.strip()

    return name, props

def parse(text_repr):
    text_repr = text_repr.split('\n')

    root = Tag('Root')

    last_item = root
    last_indent = 0
    last_at_depth = {0: root}

    for line in text_repr[2:]:
        depth = get_indent_level(line)
        name, props = parse_line(line)
        current_item = Tag(name, props)

        if depth > last_indent:
            associate(parent=last_item, child=current_item)

        if depth == last_indent:
            associate(parent=last_item.parent, child=current_item)

        if depth < last_indent:
            associate(parent=last_at_depth[depth].parent, child=current_item)

        last_item = current_item
        last_indent = depth
        last_at_depth[depth] = current_item

    return root


if __name__ == '__main__':
    parsed = parse(example_text)
    print(parsed)
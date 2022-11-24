import load_ir_from_text as lift
from clojure_to_jsx.Jsxify import to_jsx
from ir_utils import index

def select(id_):
    ir_file = open('./ir', 'r')
    lines = ir_file.read()
    print(lines)

    ir = lift.parse(lines)

    id_map = index(ir)
    print(id_map)

    make_selection(id_, id_map)

    jsx = to_jsx(ir)

    file = open('../webapp/displayer/src/Components/GeneratedApp.js', 'w')
    file.write(jsx)
    file.close()
    return '0'

def make_selection(id_, id_map):
    item = id_map[int(id_)]
    item.props['selected'] = '" "'

if __name__ == '__main__':
    select(10)
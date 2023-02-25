from clojure_to_jsx.Jsxify import to_jsx


def select(id_, ir, id_map):
    make_selection(id_, id_map)

    print('ir', ir)
    jsx = to_jsx([ir])
    print('jsx', jsx)

    file = open('../webapp/displayer/src/Components/GeneratedApp.js', 'w')
    file.write(jsx)
    file.close()
    return '0'


def make_selection(id_, id_map):
    item = id_map[int(id_)]
    item.props['selected'] = '" "'


if __name__ == '__main__':
    select(10, None, {})
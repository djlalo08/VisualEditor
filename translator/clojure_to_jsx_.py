from translator.clj_example import clojure_code
from translator.clojure_to_jsx.Jsxify import to_jsx
from translator.clojure_to_jsx.Tagify import to_tag
from translator.clojure_to_jsx.parser import parse

if __name__ == '__main__':
    parsed = parse(clojure_code)
    print('parsed\n', parsed)

    tagged = to_tag(parsed)
    print('tagged\n', tagged)

    jsx = to_jsx(tagged)
    print('jsx\n', jsx)
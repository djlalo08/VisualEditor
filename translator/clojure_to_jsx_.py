from translator.clj_example import clojure_code
from translator.clojure_to_jsx.Annotater import annotate
from translator.clojure_to_jsx.Jsxify import to_jsx_, to_jsx
from translator.clojure_to_jsx.Tagify import to_tag
from translator.clojure_to_jsx.parser import parse

if __name__ == '__main__':

    parsed = parse(clojure_code)
    # print('parsed\n', parsed)

    annotated = annotate(parsed)
    # print('annotated\n', annotated)

    tagged = to_tag(parsed)
    # print('tagged\n', tagged)

    jsx = to_jsx(tagged)
    print(jsx)
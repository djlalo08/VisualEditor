import load_ir_from_text as lift
from translator.clj_example import clojure_code
from translator.clojure_to_jsx.Annotater import annotate
from translator.clojure_to_jsx.Jsxify import to_jsx
from translator.clojure_to_jsx.parser import parse
from translator.clojure_to_jsx.Tagify import to_tag

if __name__ == '__main__':

    parsed = parse(clojure_code)
    print('parsed\n', parsed)

    annotated = annotate(parsed)
    print('annotated\n', annotated)

    # ir = to_tag(parsed)
    # print('tagged\n', ir)
    ir = lift.parse(lift.example_text)

    jsx = to_jsx(ir)
    print(jsx)

    file = open('../webapp/displayer/src/Components/GeneratedApp.js', 'w')
    file.write(jsx)
    file.close()
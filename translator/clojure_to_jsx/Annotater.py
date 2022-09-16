from translator.clojure_to_jsx.ParentedCollection import ParentedCollection
from translator.clojure_to_jsx.ParentedList import ParentedList


def annotate(parsed):
    if not isinstance(parsed, ParentedCollection):
        return parsed
    if isinstance(parsed, ParentedList) and len(parsed.ls) and parsed.ls[0] == 'm':
        [_, meta, callee] = parsed.ls
        callee.meta = meta.ls
        callee.ls = [annotate(item) for item in callee.ls]
        return callee
    parsed.ls = [annotate(item) for item in parsed.ls]
    return parsed
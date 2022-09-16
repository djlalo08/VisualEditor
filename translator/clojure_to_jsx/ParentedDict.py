from translator.clojure_to_jsx.ParentedCollection import ParentedCollection


def dict_item_str(item):
    (k, v) = item
    return str(k) + ': ' + str(v)

class ParentedDict(ParentedCollection):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ls = {}

    def __str__(self):
        res = '{'
        res += ','.join(map(dict_item_str, self.ls.items()))
        return res + '}'

    def __repr__(self):
        res = '{'
        res += ','.join(map(repr, self.ls.items()))
        return res + '}'

    def __iter__(self):
        return self.ls.items().__iter__()
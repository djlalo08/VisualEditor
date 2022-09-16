from translator.clojure_to_jsx.ParentedDict import ParentedDict
from translator.clojure_to_jsx.ParentedList import ParentedList

class NoKey:
    pass
def parse(code):
    tokens = code \
        .replace('(', ' ( ') \
        .replace(')', ' ) ') \
        .replace('[', ' [ ') \
        .replace(']', ' ] ') \
        .replace('{', ' { ') \
        .replace('}', ' } ') \
        .replace(',', ' ') \
        .split()
    current_list = ParentedList()
    last_key = NoKey()
    for token in tokens:
        if token in ['(', '[']:
            new_list = ParentedList(current_list)
            current_list.ls.append(new_list)
            current_list = new_list
        elif token in [')', ']']:
            current_list = current_list.parent
        elif token == '}':
            current_list = current_list.parent
            last_key = NoKey()
        elif token == '{':
            new_dict = ParentedDict(current_list)
            current_list.ls.append(new_dict)
            current_list = new_dict
        else:
            if isinstance(current_list, ParentedList):
                current_list.ls.append(token)
            if isinstance(current_list, ParentedDict):
                if isinstance(last_key, NoKey):
                    last_key = token.strip('"')
                else:
                    current_list.ls[last_key] = token
                    last_key = NoKey()
    return current_list.ls[0]
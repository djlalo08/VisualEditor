from translator.clojure_to_jsx.ParentedList import ParentedList

def parse(code):
    tokens = code \
        .replace('(', ' ( ') \
        .replace(')', ' ) ') \
        .replace('[', ' [ ') \
        .replace(']', ' ] ') \
        .split()
    current_list = ParentedList()
    for token in tokens:
        if token in ['(', '[']:
            new_list = ParentedList(current_list)
            current_list.ls.append(new_list)
            current_list = new_list
        elif token in [')', ']']:
            current_list = current_list.parent
        else:
            current_list.ls.append(token)
    return current_list.ls[0]
from EditorWindow import EditorWindow
from utils.string import sanitize
from Tree import RootNode


class Evaluator:

    @staticmethod
    def to_ast(event=None):
        outValues = map(lambda out: out.value, EditorWindow.outs)
        program = RootNode(list(outValues))
        print(program)
        print()
        return program

    @staticmethod
    def to_code(event=None):
        program = Evaluator.to_ast()
        reduced = program.reduce(([], set()))
        header = '''public static Object[] '''+sanitize(EditorWindow.file_name or 'D E F A U L T')+'''(Object... in){ Object[] out = new Object[''' + str(len(EditorWindow.outs)) + '''];\n\t'''
        fn_decls = '\n\t'.join(reduced)
        footer = "\n\treturn out;\n}"
        result = header + fn_decls + footer
        print(result)
        return result

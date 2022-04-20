from Canvas import Canvas
from Tree import Node

class Evaluator:

    @staticmethod
    def to_ast(event=None):
        outValues = map(lambda out: out.value, Canvas.outs)
        program = Node("root", None, list(outValues))
        print(program)
        print()
        return program

    @staticmethod
    def to_code(event=None):
        program = Evaluator.to_ast()
        reduced = program.reduce(([], set()))
        header = '''public static Object[] example(Object[] in){
        Object[] out = new Object[''' + str(len(Canvas.outs)) + '''];'''
        fn_decls = '\n\t'.join(reduced)
        footer = "\treturn out;\n}"
        print(header)
        print('\t' + fn_decls)
        print(footer)

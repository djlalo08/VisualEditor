from Canvas import Canvas
from Tree import Node


class Evaluator:

    def to_ast(self, event=None):
        outValues = map(lambda out: out.value, Canvas.outs)
        program = Node("root", None, list(outValues))
        print(program)
        print()
        return program

    def to_code(self, event=None):
        program = self.to_ast()
        reduced = program.reduce(([], set()))
        header = '''public static Object[] example(Object[] in){
        Object[] out = new Object[''' + str(len(Canvas.outs)) + '''];'''
        fn_decls = '\n\t'.join(reduced)
        footer = "\treturn out;\n}"
        print(header)
        print('\t' + fn_decls)
        print(footer)

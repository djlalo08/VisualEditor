from xxlimited import foo
from Canvas import Canvas
from Tree import RootNode

class Evaluator:

    @staticmethod
    def to_ast(event=None):
        outValues = map(lambda out: out.value, Canvas.outs)
        program = RootNode(list(outValues))
        print(program)
        print()
        return program

    @staticmethod
    def to_code(event=None):
        program = Evaluator.to_ast()
        reduced = program.reduce(([], set()))
        header = '''public static Object[] example(Object[] in){
    Object[] out = new Object[''' + str(len(Canvas.outs)) + '''];\n\t'''
        fn_decls = '\n\t'.join(reduced)
        footer = "\n\treturn out;\n}"
        result = header + fn_decls + footer
        print(result)
        return result

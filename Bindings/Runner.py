import os
from StringUtils import sanitize
from Bindings.Evaluator import Evaluator
from Canvas import Canvas

def dereference(code, retrieved_fns):
    new_code = ''
    for line in code.split('\n'):
        new_line = line
        if '#' in line:
            [front, file_name, end] = line.split('#')
            if file_name not in retrieved_fns:
                with open('lib/bin/'+file_name, 'r') as file:
                    files_code = dereference(file.read(), retrieved_fns)
                    new_code = files_code + '\n' + new_code
                    retrieved_fns.add(file_name)
            method_name = file_name.replace('.exec', '')
            new_line = front + sanitize(method_name) + end
        new_code += '\n' + new_line
    return new_code

def run(file_name, ins, outs):
    code = Evaluator.to_code()
    retrieved_fns = set()
    new_code = dereference(code, retrieved_fns)
    imports = '''
import java.io.File;
import java.io.FileWriter;
import java.io.IOException; 
'''
    args = []
    for entry in ins:
        args.append(entry.get())
    method_call = sanitize(file_name or 'D E F A U L T') + '(' + ','.join(args) + ');'

    main = \
''' public static void main(String[] args) throws IOException {\n\t''' +\
'Object[] result = ' + method_call +\
'''
File data_bus = new File("data_bus.txt");
data_bus.createNewFile();

FileWriter writer = new FileWriter("data_bus.txt");
for (Object o: result)
    writer.write(o + "\\n");
writer.close();
}
'''
    final_code = imports \
            + 'public class Transpiler {\n'\
            + main + '\n'\
            + new_code + '\n'\
            + '}'
    with open('Transpiler.java', 'w') as file:
        file.write(final_code)
    os.system("javac Transpiler.java")
    os.system("java Transpiler")
    
    result = ''
    with open('data_bus.txt', 'r') as file:
        result = file.read()
        print(result)
    for entry, output in zip(outs, result.split('\n')):
        entry.set(output)
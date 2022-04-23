import os
import tkinter as tk
from StringUtils import sanitize
from Bindings.Evaluator import Evaluator

IMPORTS = '''import java.io.File;
import java.io.FileWriter;
import java.io.IOException; 
'''

def main(method_call):
    return \
        ''' public static void main(String[] args) throws IOException {\n\t''' +\
        'Object[] result = ' + method_call + ''';
        File data_bus = new File("data_bus.txt");
        data_bus.createNewFile();

        FileWriter writer = new FileWriter("data_bus.txt");
        for (Object o: result)
            writer.write(o + "\\n");
        writer.close();
        }
        '''

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

def run(file_name, ins):
    code = Evaluator.to_code()
    retrieved_fns = set()
    new_code = dereference(code, retrieved_fns)

    args = map(tk.StringVar.get, ins)
    method_call = sanitize(file_name or 'D E F A U L T') + '(' + ','.join(args) + ')'

    final_code = IMPORTS \
            + 'public class Transpiler {\n'\
            + main(method_call) + '\n'\
            + new_code + '\n'\
            + '}'

    update_and_run_transpiler(final_code)
    return read_answer_from_data_bus()

def read_answer_from_data_bus():
    with open('data_bus.txt', 'r') as file:
        result = file.read()
        print(result)
        return result.split('\n')

def update_and_run_transpiler(final_code):
    with open('Transpiler.java', 'w') as file:
        file.write(final_code)
    os.system("javac Transpiler.java")
    os.system("java Transpiler")
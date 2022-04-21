from os import stat
import os
import pickle
import time
import tkinter as tk
from Bindings.Evaluator import Evaluator
from Interface.MapInterface import MapInterface
from Interface.MapInterfaceNode import MapInterfaceNode
from Utils import Stream
from Canvas import Canvas

class RunModal(tk.Toplevel):
    def __init__(self) -> None:
        super().__init__(Canvas.root)

        self.ins = []
        for _ in Canvas.ins:
            self.ins.append(tk.StringVar())

        self.outs = []
        for _ in Canvas.outs:
            self.outs.append(tk.StringVar())

        self.run_modal()
        self.bind('<Return>', self.run)

    @staticmethod
    def dereference(code, retrieved_fns):
        new_code = ''
        for line in code.split('\n'):
            new_line = line
            if '#' in line:
                [front, file_name, end] = line.split('#')
                if file_name not in retrieved_fns:
                    with open('lib/bin/'+file_name, 'r') as file:
                        files_code = RunModal.dereference(file.read(), retrieved_fns)
                        new_code = files_code + '\n' + new_code
                        retrieved_fns.add(file_name)
                method_name = file_name.replace('.exec', '')
                new_line = front + method_name + end
            new_code += '\n' + new_line
        return new_code

    def run(self, event=None):
        code = Evaluator.to_code()
        retrieved_fns = set()
        new_code = RunModal.dereference(code, retrieved_fns)
        imports = '''
import java.io.File;
import java.io.FileWriter;
import java.io.IOException; 
'''
        args = []
        for entry in self.ins:
            args.append(entry.get())
        method_call = Canvas.file_name + '(' + ','.join(args) + ');'

        main = \
''' public static void main(String[] args) throws IOException {''' +\
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
        for entry, output in zip(self.outs, result.split('\n')):
            entry.set(output)
            
        
    def run_modal(self):
        self.title('Run ' + Canvas.file_name)

        in_label = tk.Label(self, text = 'ins').place(x = 40, y = 20)  
        ins = []
        for idx, _ in enumerate(Canvas.ins):
            input = tk.Entry(self, width = 30, textvariable=self.ins[idx])
            input.place(x = 110, y = 20+40*idx)
            ins.append(input)
        if ins and ins[0]:
            ins[0].focus()

        out_label = tk.Label(self, text = 'outs').place(x = 40, y = len(ins)*40+60)  
        outs = []
        for idx, _ in enumerate(Canvas.outs):
            output = tk.Entry(self, width = 30, textvariable=self.outs[idx])
            output.place(x = 110, y = (len(ins)+idx)*40+60)
            output.config(state='readonly')
            outs.append(output)

        submit_button = tk.Button(self, text = 'Run', command=self.run).place(x = 332, y = (len(ins)+len(outs))*40+60)

        y = (len(ins)+len(outs))*40+100
        self.geometry('460x' + str(y))
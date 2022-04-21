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
        self.ins = [tk.StringVar()]*len(Canvas.ins)
        self.outs = [tk.StringVar()]*len(Canvas.outs)
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
        imports = 'import java.util.Arrays;'
        main = 'public static void main(String[] args) {\n\t System.out.println("hi");\n}'
        final_code = imports + '\n\n'\
                + 'public class Transpiler {\n'\
                + main + '\n'\
                + new_code + '\n'\
                + '}'
        with open('Transpiler.java', 'w') as file:
            file.write(final_code)
        os.system("javac Transpiler.java")
        os.system("java Transpiler")
        
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
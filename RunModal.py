from os import stat
import pickle
import tkinter as tk
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

    def run(self, event=None):
        pass
        
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
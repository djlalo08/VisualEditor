import tkinter as tk
from EditorWindow import EditorWindow
from actors.runner import run

class RunModal(tk.Toplevel):
    def __init__(self) -> None:
        super().__init__(EditorWindow.root)

        self.ins = []
        for _ in EditorWindow.ins:
            self.ins.append(tk.StringVar())

        self.outs = []
        for _ in EditorWindow.outs:
            self.outs.append(tk.StringVar())

        self.run_modal()
        self.bind('<Return>', self.run_)

    def run_(self, event=None):
        results = run(EditorWindow.file_name, self.ins)
        for entry, output in zip(self.outs, results):
            entry.set(output)
        
    def run_modal(self):
        self.title('Run ' + EditorWindow.file_name)

        in_label = tk.Label(self, text = 'ins').place(x = 40, y = 20)  
        ins = []
        for idx, _ in enumerate(EditorWindow.ins):
            input = tk.Entry(self, width = 30, textvariable=self.ins[idx])
            input.place(x = 110, y = 20+40*idx)
            ins.append(input)
        if ins and ins[0]:
            ins[0].focus()

        out_label = tk.Label(self, text = 'outs').place(x = 40, y = len(ins)*40+60)  
        outs = []
        for idx, _ in enumerate(EditorWindow.outs):
            output = tk.Entry(self, width = 30, textvariable=self.outs[idx])
            output.place(x = 110, y = (len(ins)+idx)*40+60)
            output.config(state='readonly')
            outs.append(output)

        submit_button = tk.Button(self, text = 'Run', command=self.run_).place(x = 332, y = (len(ins)+len(outs))*40+60)

        y = (len(ins)+len(outs))*40+100
        self.geometry('460x' + str(y))
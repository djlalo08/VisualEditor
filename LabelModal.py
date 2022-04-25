from cProfile import label
import pickle
import tkinter as tk
from Interface.MapInterface import MapInterface
from Interface.MapInterfaceNode import MapInterfaceNode
from Interface.InterfaceLabels import InterfaceLabels
from Utils import Stream

pad_lr = 20
pad_tb = 20
t_h = 20 # text height
t_w = 40 # text width

class LabelModal(tk.Toplevel):
    def __init__(self, root, ins, outs, fn_name='', labels=None) -> None:
        super().__init__(root, background='#E7B680')
        self.root = root
        self.fn_name = fn_name
        self.ins = ins
        self.outs = outs
        
        self.center = tk.StringVar()
        self.top = tk.StringVar()
        self.bot = tk.StringVar()
        self.left = tk.StringVar()
        self.right = tk.StringVar()
        
        self.in_tops = self.string_var_list(ins)
        self.in_btwns = self.string_var_list(range( len(ins)+1 ))
        self.in_bots = self.string_var_list(ins)

        self.out_tops = self.string_var_list(outs)
        self.out_btwns = self.string_var_list(range( len(outs)+1 ))
        self.out_bots = self.string_var_list(outs)
        
        self.all_vars = [self.center, self.top, self.bot, self.left, self.right] + self.in_tops + self.in_btwns + self.in_bots + self.out_tops + self.out_btwns + self.out_bots
        
        self.update_labels(labels)

        self.new_map_modal()
        self.bind('<Command-s>', self.save)
        
    def update_labels_row(self, stringVars, oldVals):
        for stringVar, oldVal in zip(stringVars, oldVals):
            stringVar.set(oldVal)

    def update_labels(self, labels):
        if not labels: return
        
        self.center.set(labels.center)
        self.top.set(labels.top)
        self.bot.set(labels.bot)
        self.left.set(labels.left)
        self.right.set(labels.right)
        
        self.update_labels_row(self.in_tops, labels.in_tops)
        self.update_labels_row(self.in_btwns, labels.in_btwns)
        self.update_labels_row(self.in_bots, labels.in_bots)

        self.update_labels_row(self.out_tops, labels.out_tops)
        self.update_labels_row(self.out_btwns, labels.out_btwns)
        self.update_labels_row(self.out_bots, labels.out_bots)

    def string_var_list(self, ins):
        ls = []
        for _ in ins:
            ls.append(tk.StringVar())
        return ls

    def collect_labels(self):
        in_tops = list(map(tk.StringVar.get, self.in_tops))
        in_btwns = list(map(tk.StringVar.get, self.in_btwns))
        in_bots = list(map(tk.StringVar.get, self.in_bots))

        out_tops = list(map(tk.StringVar.get, self.out_tops))
        out_btwns = list(map(tk.StringVar.get, self.out_btwns))
        out_bots = list(map(tk.StringVar.get, self.out_bots))
        
        return InterfaceLabels(self.fn_name, self.center.get(), 
            self.top.get(), self.bot.get(), 
            self.left.get(), self.right.get(), 
            in_tops, in_btwns, in_bots, 
            out_tops, out_btwns, out_bots)
        
    def save(self, event=None):
        labels = self.collect_labels()
        self.root.submit(label=labels)
        
    def new_map_modal(self):
        self.title("Set map info")
        w_count = max(len(self.ins), len(self.outs))
        tot_h = 9*t_h # (not including padding)
        tot_w = (2*w_count + 3)*t_w # (not including padding)
        win_h = tot_h + 2*pad_tb
        win_w = tot_w + 2*pad_lr

        self.geometry(str(win_w) + 'x' + str(win_h))
        
        self.entry(self.top, x=t_w, y=0, w=tot_w - 2*t_w)
        self.entry(self.bot, x=t_w, y=8*t_h, w=tot_w - 2*t_w)
        center = self.entry(self.center, x=t_w, y=4*t_h, w=tot_w - 2*t_w)
        self.entry(self.left, x=0, y=4*t_h) 
        self.entry(self.right, x=tot_w-t_w, y=4*t_h)
        
        self.entry_row(self.in_tops, 1, 2)
        self.entry_row(self.in_btwns, 2, 1)
        self.entry_row(self.in_bots, 3, 2)
        self.entry_row(self.out_tops, 5, 2)
        self.entry_row(self.out_btwns, 6, 1)
        self.entry_row(self.out_bots, 7, 2)

        self.label_row(self.ins, 2, 2)
        self.label_row(self.outs, 6, 2)

        center.focus()
        if not any(map(tk.StringVar.get, self.all_vars)):
            self.center.set(self.fn_name)
        # submit_button = tk.Button(self, text = "Done", command=self.submit).place(x = 250, y = 140)
        
    def label(self, text, x, y):
        x+= pad_lr
        y+= pad_tb
        t = tk.Label(self, text=text, background='white', borderwidth=2, relief="solid")
        t.place(x=x, y=y, width=t_w, height=t_h)
        return t
    
    def label_row(self, labels, row, offset):
        for i, label in enumerate(labels):
            self.label(label, (2*i+offset)*t_w, row*t_h)
        
    def entry_row(self, vars, row, offset):
        for i, entry in enumerate(vars):
            self.entry(entry, (2*i+offset)*t_w, row*t_h)
        
    def entry(self, var, x, y, w=t_w, h=t_h, incl_lr_pad=True, incl_tb_pad=True):
        if incl_lr_pad: x+= pad_lr
        if incl_tb_pad: y+= pad_tb
        e = tk.Entry(self, textvariable=var, justify='center', background='#F8F2DE', highlightcolor='#F8F2DE', highlightbackground='#E7B680')
        e.place(x=x, y=y, width=w, height=h)
        return e
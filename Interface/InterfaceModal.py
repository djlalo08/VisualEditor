
import pickle
import tkinter as tk
from Interface.MapInterface import MapInterface
from Interface.MapInterfaceNode import MapInterfaceNode
from Utils import Stream
from LabelModal import LabelModal

class InterfaceModal(tk.Toplevel):
    def __init__(self, root) -> None:
        super().__init__(root)
        self.root = root
        self.fn_name = tk.StringVar()
        self.ins = tk.StringVar()
        self.outs = tk.StringVar()
        self.labels = None
        self.new_map_modal()
        self.bind('<Return>', self.submit)
        self.bind('<Command-o>', self.load)

    def load(self, event=None):
        fn_name = self.fn_name.get()

        with open('lib/int/'+fn_name+'.Int', 'rb') as file:
            interface = pickle.load(file)
            self.ins.set( str(interface.ins) )
            self.outs.set( str(interface.outs) )
            self.labels = interface.labels
         

    def submit(self, event=None, label=None):
        fn_name, ins, outs = self.read_fields()
        self.save_int(fn_name, ins, outs, label)
        self.destroy()
        self.root.destroy()

    def set_labels(self, event=None):
        fn_name, ins, outs = self.read_fields()
        LabelModal(self, ins, outs, fn_name, self.labels)

    def read_fields(self):
        fn_name = self.fn_name.get()
        ins = self.ins.get()
        ins = ins.split(",") if ins else ''
        outs = self.outs.get()
        outs = outs.split(",") if outs else ''
        return fn_name, ins, outs
        
    def save_int(self, name, ins, outs, label=None):
        ins = Stream(ins).map(lambda in_name: MapInterfaceNode(in_name, 'type')).to_list()
        outs = Stream(outs).map(lambda out_name: MapInterfaceNode(out_name, 'type')).to_list()
        interface = MapInterface(name, ins, outs, '', labels=label)
        with open('lib/int/'+name+'.Int', 'wb') as file:
            pickle.dump(interface, file)
        
    def new_map_modal(self):
        self.title("Set map info")
        self.geometry("460x180")

        fn_name_label = tk.Label(self, text = "fn name").place(x = 40, y = 20)  
        fn_name = tk.Entry(self, width = 30, textvariable=self.fn_name)
        fn_name.place(x = 110, y = 20)  
        fn_name.focus()

        in_label = tk.Label(self, text = "ins").place(x = 40, y = 60)  
        ins = tk.Entry(self, width = 30, textvariable=self.ins).place(x = 110, y = 60)  

        out_label = tk.Label(self, text = "outs").place(x = 40, y = 100)  
        outs = tk.Entry(self, width = 30, textvariable=self.outs).place(x = 110, y = 100)  

        labels_button = tk.Button(self, text = "Set Labels", command=self.set_labels).place(x = 100, y = 140)

        submit_button = tk.Button(self, text = "Give me a map!", command=self.submit).place(x = 250, y = 140)

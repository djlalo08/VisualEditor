
import pickle
import tkinter as tk
from Interface.MapInterface import MapInterface
from Interface.MapInterfaceNode import MapInterfaceNode
from Utils import Stream

class InterfaceModal(tk.Toplevel):
    def __init__(self, root) -> None:
        super().__init__(root)
        self.root = root
        self.fn_name = tk.StringVar()
        self.ins = tk.StringVar()
        self.outs = tk.StringVar()
        self.new_map_modal()
        self.bind('<Return>', self.submit)

    def submit(self, event=None):
        fn_name = self.fn_name.get()
        ins = self.ins.get()
        ins = ins.split(",") if ins else ''
        outs = self.outs.get().split(",")
        self.save_int(fn_name, ins, outs)
        self.destroy()
        self.root.destroy()
        
    def save_int(self, name, ins, outs):
        ins = Stream(ins).map(lambda in_name: MapInterfaceNode(in_name, 'type')).to_list()
        outs = Stream(outs).map(lambda out_name: MapInterfaceNode(out_name, 'type')).to_list()
        interface = MapInterface(name, ins, outs, '')
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

        submit_button = tk.Button(self, text = "Give me a map!", command=self.submit).place(x = 250, y = 140)
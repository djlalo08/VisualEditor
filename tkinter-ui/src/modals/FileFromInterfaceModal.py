import pickle
import tkinter as tk

from EditorWindow import EditorWindow
from GlobalData import resources
from actors.wire_adder import WireAdder


class FileFromInterfaceModal(tk.Toplevel):
    def __init__(self) -> None:
        super().__init__(EditorWindow.root)
        self.fn_name = tk.StringVar()
        self.create_modal()
        self.bind('<Return>', self.submit)

    def submit(self, event):
        fn_name = self.fn_name.get()
        self.load_file(fn_name)
        self.destroy()

    @staticmethod
    def load_file(name):
        with open(f'{resources}/lib/int/{name}.Int', 'rb') as file:
            interface = pickle.load(file)
            for _ in interface.ins:
                WireAdder.add_in_wire()

            for _ in interface.outs:
                WireAdder.add_out_wire()

    def create_modal(self):
        self.title("New Map From Interface:")
        self.geometry("460x100")

        fn_name_label = tk.Label(self, text="fn name").place(x=40, y=20)
        fn_name = tk.Entry(self, width=30, textvariable=self.fn_name)
        fn_name.place(x=110, y=20)
        fn_name.focus()

        submit_button = tk.Button(self, text="Open", command=self.submit).place(x=100, y=60)

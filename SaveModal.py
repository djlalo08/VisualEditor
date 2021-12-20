import pickle
import tkinter as tk
from Canvas import Canvas

class SaveModal(tk.Toplevel):
    def __init__(self) -> None:
        super().__init__(Canvas.root)
        self.fn_name = tk.StringVar()
        self.save_modal()

    def submit(self):
        fn_name = self.fn_name.get()
        self.save_as(fn_name)
        self.destroy()
            
    @staticmethod
    def save_as(name):
        with open('lib/'+name, 'wb') as file:
            pickle.dump(Canvas.id_map, file)
            pickle.dump(Canvas.out_refs, file)

    def save_modal(self):
        self.title("Save Map As:")
        self.geometry("460x100")

        fn_name_label = tk.Label(self, text = "fn name").place(x = 40, y = 20)  
        fn_name = tk.Entry(self, width = 30, textvariable=self.fn_name).place(x = 110, y = 20)  

        submit_button = tk.Button(self, text = "Save", command=self.submit).place(x = 100, y = 60)
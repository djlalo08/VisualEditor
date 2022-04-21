import pickle
import tkinter as tk
from Canvas import Canvas
from Bindings.Evaluator import Evaluator

#In reality I should extract save functionality into a binding and this should be the save as modal, which can call the Saver.save(file_name)

class SaveModal(tk.Toplevel):
    def __init__(self, save_as = False) -> None:
        super().__init__(Canvas.root)
        if Canvas.file_name and not save_as:
            self.save_as(Canvas.file_name)
            self.destroy()
            return
        self.fn_name = tk.StringVar()
        self.save_modal()
        self.bind('<Return>', self.submit)

    def submit(self, event):
        fn_name = self.fn_name.get()
        self.save_as(fn_name)
        self.destroy()
            
    @staticmethod
    def save_as(name):
        with open('lib/src/'+name, 'wb') as file:
            pickle.dump(Canvas.id_map, file)
            pickle.dump(Canvas.ins, file)
            pickle.dump(Canvas.outs, file)

        with open('lib/bin/'+name+'.exec', 'w') as file:
            file.write(Evaluator.to_code())
            
        Canvas.file_name = name
        Canvas.root.title(name)

    def save_modal(self):
        self.title("Save Map As:")
        self.geometry("460x100")

        fn_name_label = tk.Label(self, text = "fn name").place(x = 40, y = 20)  
        fn_name = tk.Entry(self, width = 30, textvariable=self.fn_name)
        fn_name.place(x = 110, y = 20)  
        fn_name.focus()

        submit_button = tk.Button(self, text = "Save", command=self.submit).place(x = 100, y = 60)
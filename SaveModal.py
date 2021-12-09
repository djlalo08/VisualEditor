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
            pickle.dump(len(Canvas.id_map), file)
            for key, value in Canvas.id_map.items():
                value.prep_for_save()
            for key in Canvas.id_map:
                obj = Canvas.id_map.get(key)
                pickle.dump(obj, file)

            o_ids = list(map(lambda o: o.id, Canvas.outs))
            pickle.dump(o_ids, file)

            for key, value in Canvas.id_map.items():
                value.prep_from_save_for_use(Canvas.canvas, Canvas.id_map)

    def save_modal(self):
        self.title("Save Map As:")
        self.geometry("460x100")

        fn_name_label = tk.Label(self, text = "fn name").place(x = 40, y = 20)  
        fn_name = tk.Entry(self, width = 30, textvariable=self.fn_name).place(x = 110, y = 20)  

        submit_button = tk.Button(self, text = "Save", command=self.submit).place(x = 100, y = 60)
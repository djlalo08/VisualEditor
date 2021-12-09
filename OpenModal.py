import pickle
import tkinter as tk
from Canvas import Canvas

class OpenModal(tk.Toplevel):
    def __init__(self) -> None:
        super().__init__(Canvas.root)
        self.fn_name = tk.StringVar()
        self.open_modal()

    def submit(self):
        fn_name = self.fn_name.get()
        self.load_file(fn_name)
        self.destroy()
        
    @staticmethod
    def load_file(name):
        with open('lib/'+name, 'rb') as file:
            num_items = pickle.load(file)
            items = []
            for _ in range(num_items):
                item = pickle.load(file)
                item.canvas = Canvas.canvas
                items.append(item)

            for item in items:
                item.id = item.build_obj()
                Canvas.id_map[item.id] = item
                item.id_map = Canvas.id_map
                print("success. Item id: ", item.id)

            out_ids = pickle.load(file)
            Canvas.outs = list(map(lambda o_id: Canvas.id_map[o_id], out_ids))

            for item in items:
                item.prep_from_save_for_use(Canvas.canvas, Canvas.id_map) 
            
            for item in items:
                item.update()
            
    def open_modal(self):
        self.title("Open Map:")
        self.geometry("460x100")

        fn_name_label = tk.Label(self, text = "fn name").place(x = 40, y = 20)  
        fn_name = tk.Entry(self, width = 30, textvariable=self.fn_name).place(x = 110, y = 20)  

        submit_button = tk.Button(self, text = "Save", command=self.submit).place(x = 100, y = 60)
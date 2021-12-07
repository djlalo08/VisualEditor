import tkinter as tk

class MapModal(tk.Toplevel):
    def __init__(self, canvas) -> None:
        super().__init__(canvas)
        self.new_map_modal()

    def submit(self):
        self.destroy()
            
    def new_map_modal(self):
        self.title("Set map info")
        self.geometry("460x180")

        fn_name_label = tk.Label(self, text = "fn name").place(x = 40, y = 20)  
        fn_name = tk.Entry(self, width = 30).place(x = 110, y = 20)  

        in_label = tk.Label(self, text = "ins").place(x = 40, y = 60)  
        ins = tk.Entry(self, width = 30).place(x = 110, y = 60)  

        out_label = tk.Label(self, text = "outs").place(x = 40, y = 100)  
        outs = tk.Entry(self, width = 30).place(x = 110, y = 100)  

        submit_button = tk.Button(self, text = "Give me a map!", command=self.submit).place(x = 250, y = 140)
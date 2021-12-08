import tkinter as tk

class OpenModal(tk.Toplevel):
    def __init__(self, root) -> None:
        super().__init__(root)
        self.root = root
        self.fn_name = tk.StringVar()
        self.open_modal()

    def submit(self):
        fn_name = self.fn_name.get()
        self.root.load_file(fn_name)
        self.destroy()
            
    def open_modal(self):
        self.title("Open Map:")
        self.geometry("460x100")

        fn_name_label = tk.Label(self, text = "fn name").place(x = 40, y = 20)  
        fn_name = tk.Entry(self, width = 30, textvariable=self.fn_name).place(x = 110, y = 20)  

        submit_button = tk.Button(self, text = "Save", command=self.submit).place(x = 100, y = 60)
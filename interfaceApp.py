import tkinter as tk
from Interface.InterfaceModal import InterfaceModal
    
class InterfaceApp(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        InterfaceModal(self)

if __name__ == "__main__":
    root = tk.Tk()
    InterfaceApp(root).pack(fill="both", expand=True)
    root.mainloop()
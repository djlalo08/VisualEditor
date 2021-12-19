import tkinter as tk
from Canvas import Canvas
from firstfile import Bindings

if __name__ == "__main__":
    root = tk.Tk()
    Canvas(root).pack(fill="both", expand=True)
    binder = Bindings()
    binder.set_bindings()
    root.mainloop()
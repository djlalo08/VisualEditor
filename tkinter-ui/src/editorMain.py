import tkinter as tk

from EditorWindow import EditorWindow
from firstfile import Bindings

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry(f'{1000}x{500}')

    ew = EditorWindow(root)
    ew.pack(fill='both', expand=True)

    binder = Bindings(ew)
    binder.set_bindings()

    root.mainloop()

import tkinter as tk
from EditorWindow import EditorWindow
from firstfile import Bindings

if __name__ == "__main__":
    root = tk.Tk()
    EditorWindow(root)
    binder = Bindings()
    binder.set_bindings()
    root.mainloop()
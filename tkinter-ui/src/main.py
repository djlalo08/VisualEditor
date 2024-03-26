import tkinter as tk

from EditorWindow import EditorWindow
from firstfile import Bindings

if __name__ == "__main__":
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    screen_height = 900
    root.geometry(f'{screen_width}x{screen_height}')

    row_weights = [2, 1]
    for index, weight in enumerate(row_weights):
        root.grid_rowconfigure(index, weight=weight)

    col_weights = [1, 3, 1]
    for index, weight in enumerate(col_weights):
        root.grid_columnconfigure(index, weight=weight)

    ew = EditorWindow(root)
    ew.grid(row=0, column=1, sticky="nsew")
    binder = Bindings(ew)
    binder.set_bindings()

    bot_pane = tk.Frame(root, background="gray")
    bot_pane.grid(row=1, column=0, sticky="nsew", columnspan=3, padx=5, pady=2)

    b = tk.Button(bot_pane, text="Somthin")
    b.pack()

    right_pane = tk.Frame(root, background="red")
    right_pane.grid(row=0, column=2, sticky="nsew", padx=1, pady=1)

    b2 = tk.Button(right_pane, text="Somthin")
    b2.pack()

    left_pane = tk.Frame(root, background="blue")
    left_pane.grid(row=0, column=0, sticky="nsew", padx=5, pady=2)

    b3 = tk.Button(left_pane, text="Somthin")
    b3.pack()

    root.mainloop()

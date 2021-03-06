from EditorWindow import EditorWindow


def cursorxy():
    c = EditorWindow.canvas
    (x_abs, y_abs) = c.winfo_pointerxy()
    (x_frame, y_frame) = (c.winfo_rootx(), c.winfo_rooty())
    return (x_abs - x_frame, y_abs - y_frame)

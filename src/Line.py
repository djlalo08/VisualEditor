from EditorWindow import EditorWindow
from ObjectHierarchy.Object import Object


class Line(Object):
    def __init__(self, *args, line_num, **kwargs):
        self.line_num = line_num
        super().__init__(*args, **kwargs)

    def build_obj(self):
        return EditorWindow.canvas.create_rectangle(
            self.abs_pos().around(self.width, self.height),
            outline="gray")

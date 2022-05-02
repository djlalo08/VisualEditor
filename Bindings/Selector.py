from EditorWindow import EditorWindow

class Selector:

    def select_item(self, newSelected):
        oldSelected = EditorWindow.selected
        EditorWindow.selected  = newSelected 
        if EditorWindow.selected == oldSelected:
            EditorWindow.selected = None
        else:
            self.do_selection_action(EditorWindow.selected, oldSelected)

        if oldSelected:
            oldSelected.deselect()

    def do_selection_action(self, newSelection, oldSelection):
        if EditorWindow.mode == "connect":
                newPos = newSelection.abs_pos()
                delta= newPos - oldSelection.abs_pos()
                oldSelection.move(delta)
                EditorWindow.mode = "select"
        if EditorWindow.mode == "select":
                newSelection.select()

from Canvas import Canvas

class Selector:

    def select_item(self, newSelected):
        oldSelected = Canvas.selected
        Canvas.selected  = newSelected 
        if Canvas.selected == oldSelected:
            Canvas.selected = None
        else:
            self.do_selection_action(Canvas.selected, oldSelected)

        if oldSelected:
            oldSelected.deselect()

    def do_selection_action(self, newSelection, oldSelection):
        if Canvas.mode == "connect":
                newPos = newSelection.abs_pos()
                delta= newPos - oldSelection.abs_pos()
                oldSelection.move(delta)
                Canvas.mode = "select"
        if Canvas.mode == "select":
                newSelection.select()

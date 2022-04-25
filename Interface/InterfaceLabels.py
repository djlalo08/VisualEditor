from Utils import empty_if_null
from Label import Label

def label(parent, text, row, index=-1):
    return Label(parent_ref=parent.ref, text=text, offset=parent.abs_pos(), row_name=row, index=index)

class InterfaceLabels:

    def __init__(self, name, center='', top='', bot='', left='', right='', in_tops=None, in_btwns=None, in_bots=None, out_tops=None, out_btwns=None, out_bots=None) -> None:
        self.center = center 
        self.top = top
        self.bot = bot
        self.left = left
        self.right = right

        self.in_tops = empty_if_null(in_tops)
        self.in_btwns = empty_if_null(in_btwns)
        self.in_bots = empty_if_null(in_bots)

        self.out_tops = empty_if_null(out_tops)
        self.out_btwns = empty_if_null(out_btwns)
        self.out_bots = empty_if_null(out_bots)
        
    def add_label(self, accumulator, text, row_name):
        if text:
            accumulator.append( label(self.parent, text, row_name).ref )

    def add_row(self, accumulator, label_list, row_name):
        for i, l in enumerate(empty_if_null(label_list)):
            accumulator.append( label(self.parent, l, row_name, i).ref )
        
    def create_labels(self, parent):
        self.parent = parent
        label_refs = []

        self.add_label(label_refs, self.center, 'center')
        self.add_label(label_refs, self.top, 'top')

        self.add_row(label_refs, self.in_tops, 'in_tops')
        self.add_row(label_refs, self.in_btwns, 'in_btwns')
        self.add_row(label_refs, self.in_bots, 'in_bots')

        self.add_row(label_refs, self.out_tops, 'out_tops')
        self.add_row(label_refs, self.out_btwns, 'out_btwns')
        self.add_row(label_refs, self.out_bots, 'out_bots')
        '''
        self.add_label(label_refs, self.bot, 'bot')
        self.add_label(label_refs, self.left, 'left')
        self.add_label(label_refs, self.right, 'right')
            

        '''
        
        return label_refs
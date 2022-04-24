from Utils import empty_if_null

class InterfaceLabels:

    def __init__(self, name, center='', top='', bot='', left='', right='', in_tops=None, in_btwns=None, in_bots=None, out_tops=None, out_btwns=None, out_bots=None) -> None:
        self.center = center if center else name
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
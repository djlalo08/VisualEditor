class ParentedCollection:
    def __init__(self, parent=None):
        self.ls = []
        self.parent = parent
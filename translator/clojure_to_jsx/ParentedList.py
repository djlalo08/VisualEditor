class ParentedList:
    def __init__(self, parent=None):
        self.ls = []
        self.parent = parent
        self.current_index = 0

    def __str__(self):
        res = '('
        res += ','.join(map(str, self.ls))
        return res + ')'

    def __repr__(self):
        res = '('
        res += ','.join(map(repr, self.ls))
        return res + ')'

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index >= len(self.ls):
            raise StopIteration

        res = self.ls[self.current_index]
        self.current_index += 1
        return res
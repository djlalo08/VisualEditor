class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def around(self, width, height):
        return [self.x - width / 2, self.y - height / 2, self.x + width / 2, self.y + height / 2]

    def unpack(self):
        return (self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)

    def __truediv__(self, num):
        x = self.x / num
        y = self.y / num
        return Point(x, y)

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

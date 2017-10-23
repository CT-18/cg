class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def keyX(p):
    return p.x

def keyY(p):
    return p.y

def comparePointsLists(first, second):
    if len(first) != len(second):
        return False
    first.sort(key=keyY)
    second.sort(key=keyY)
    first.sort(key=keyX)
    second.sort(key=keyX)
    s_it = iter(second)
    for f in first:
        s = s_it.__next__()
        if (f.x != s.x) or (f.y != s.y):
            return False
    return True

class Rectangle:
    def __init__(self, xMin, xMax, yMin, yMax):
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
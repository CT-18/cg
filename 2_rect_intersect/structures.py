import numpy as np

# ------------------------- ТОЧКА -------------------------

class Point:
    def __init__(self, x, y):
        self.coords = [x, y]

    @property
    def x(self):
        return self.coords[0]

    @property
    def y(self):
        return self.coords[1]

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

def medianaX(points):
    return medianaCoord(points, 0)

def medianaY(points):
    return medianaCoord(points, 1)

def medianaCoord(points, index):
    coords = []
    for p in points:
        coords.append(p.coords)
    npCoords = np.array(coords)
    return np.mean(npCoords[:, index])


# ------------------------- ПРЯМОУГОЛЬНИК -------------------------

class Rectangle:
    def __init__(self, xMin, yMin, xMax, yMax):
        self.xMin = xMin
        self.yMin = yMin
        self.xMax = xMax
        self.yMax = yMax

    def include(self, rect):
        if (rect.xMin >= self.xMin) and (rect.yMin >= self.yMin) and (rect.xMax <= self.xMax)  and (rect.yMax <= self.yMax):
            return True
        return False
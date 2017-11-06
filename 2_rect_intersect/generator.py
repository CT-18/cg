from random import randint
from structures import *

TEST_SIZE = 100

# генерация точек для визуализации
def generateVisualPoints(size_test):
    m = {}
    points = []
    repeat = size_test
    max_repeat = 400
    while (repeat > 0) and (max_repeat > 0):
        x = randint(0, 20)
        y = randint(0, 20)
        if m.get(x) is None:
            m[x] = set()
        if not (y in m[x]):
            points.append((x, y))
            m[x].add(y)
            repeat -= 1
        max_repeat -= 1    
    return points

# генератор точек для теста
def generateTestPoints():
    m = {}
    points = []
    for i in range(0, TEST_SIZE):
        point = Point(randint(-10, 10), randint(-10, 10))
        if m.get(point.x) is None:
            m[point.x] = set()
        if not (point.y in m[point.x]):
            points.append(point)
            m[point.x].add(point.y)
    return points

# генератор прямогольника для теста
def generateTestRect():
    xMin = randint(-10, 10)
    xMax = randint(-10, 10)
    if xMin > xMax:
        xMin, xMax = xMax, xMin
    yMin = randint(-10, 10)
    yMax = randint(-10, 10)
    if yMin > yMax:
        yMin, yMax = yMax, yMin
    return Rectangle(xMin, yMin, xMax, yMax)
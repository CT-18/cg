import structures

from random import randint

TEST_SIZE = 100

# генерация точек для визуализации
def generateVisualPoints(size_test):
    points = []
    for i in range(0, size_test):
        points.append((randint(0, 20), randint(0, 20)))
    return points

# генератор точек для теста
def generateTestPoints():
    m = {}
    points = []
    for i in range(0, TEST_SIZE):
        point = structures.Point(randint(-10, 10), randint(-10, 10))
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
    if (xMin > xMax):
        xMin, xMax = xMax, xMin
    yMin = randint(-10, 10)
    yMax = randint(-10, 10)
    if (yMin > yMax):
        yMin, yMax = yMax, yMin
    return structures.Rectangle(xMin, xMax, yMin, yMax)
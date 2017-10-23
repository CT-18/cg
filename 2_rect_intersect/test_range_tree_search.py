import structures
import range_tree

from random import randint

TEST_SIZE = 100

# тестирование выполнения запроса в range-tree
def testPointsInRect(testFunction):
    testPoints = generateTestPoints()
    testRect = generateTestRect()
    rangeTree = range_tree.buildRangeTree(testPoints)

    result = testFunction(rangeTree, testRect)
    expectedResult = range_tree.pointsInRectangle(rangeTree, testRect)

    if compareLists(expectedResult, result):
        print("\n------------------------- OK -------------------------\n")
    else:
        print("\n------------------------- FAIL -------------------------\n")

# генератор точек для теста
def generateTestPoints():
    points = []
    for i in range(0, TEST_SIZE):
        points.append(structures.Point(randint(-10, 10), randint(-10, 10)))
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


# ------------------------- ПРОВЕРКА -------------------------

# сравнение хранящихся в списках точек
def compareLists(first, second):
    if len(first) != len(second):
        return False
    s_it = iter(second)
    for f in first:
        s = s_it.__next__()
        if (f.x != s.x) or (f.y != s.y):
            return False
    return True

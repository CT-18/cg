import range_tree

from random import randint

TEST_SIZE = 100

def testBuildTree(testFunction):
    test = generateTest()

    result = testFunction(test)
    expectedResult = buildTree(test)

def generateTest():
    points = []

    for i in range(0, TEST_SIZE):
        points.append((randint(-10, 10), randint(-10, 10)))

    return points

def buildTree(points):
    tree = range_tree.RangeTree()

    orderedPoints = []
    xValues = []

    for x, y in points:
        if len(orderedPoints[x]) == 0:
            orderedPoints[x] = []
            xValues.append(x)

        orderedPoints[x].append(y)

    for xValue in xValues:
        tree.insert(binary_search_tree.InnerTree(xValue, orderedPoints[xValue]))

    return tree

def buildInnerTree(values):
    tree = range_tree.RangeTree()

    for val in values:
        tree.insert(val)

    return tree

def compareTrees(lhs, rhs):
    return 1

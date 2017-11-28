import generator
import kd_tree
import range_tree
from structures import *

# тестирование выполнения запроса в kd-tree
def testKdTreePointsInRect(testFunction):
    testPointsInRect(kd_tree.buildKdTree, kd_tree.pointsInRectangle, testFunction)

# тестирование выполнения запроса в range-tree
def testRangeTreePointsInRect(testFunction):
    testPointsInRect(range_tree.buildRangeTree, range_tree.pointsInRectangle, testFunction)

# вспомогательная функция для тестирования выполнения запроса в деревьях
def testPointsInRect(buildFunction, searchFunction, testFunction):
    for tests in range(0, 10):
        testPoints = generator.generateTestPoints()
        tree = buildFunction(testPoints)
        for rects in range(0, 10):
            testRect = generator.generateTestRect()
            result = testFunction(tree, testRect)
            expectedResult = searchFunction(tree, testRect)
            if not comparePointsLists(expectedResult, result):
                print("\n------------------------- FAIL -------------------------\n")
                return
    print("\n------------------------- OK -------------------------\n")
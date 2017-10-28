import structures
import generator
import kd_tree
import range_tree

# тестирование выполнения запроса в kd-tree
def testKdTreePointsInRect(testFunction):
    tests = 10
    while (tests > 0):
        tests -= 1
        testPoints = generator.generateTestPoints()
        kdTree = kd_tree.buildKdTree(testPoints)
        rects = 10
        while (rects > 0):
            rects -= 1
            testRect = generator.generateTestRect()
            result = testFunction(kdTree, testRect)
            expectedResult = kd_tree.pointsInRectangle(kdTree, testRect)
            if not structures.comparePointsLists(expectedResult, result):
                print("\n------------------------- FAIL -------------------------\n")
                return
    print("\n------------------------- OK -------------------------\n")

# тестирование выполнения запроса в range-tree
def testRangeTreePointsInRect(testFunction):
    tests = 10
    while (tests > 0):
        tests -= 1
        testPoints = generator.generateTestPoints()
        rangeTree = range_tree.buildRangeTree(testPoints)
        rects = 10
        while (rects > 0):
            rects -= 1
            testRect = generator.generateTestRect()
            result = testFunction(rangeTree, testRect)
            expectedResult = range_tree.pointsInRectangle(rangeTree, testRect)
            if not structures.comparePointsLists(expectedResult, result):
                print("\n------------------------- FAIL -------------------------\n")
                return
    print("\n------------------------- OK -------------------------\n")

# тестирование данных реализаций range-tree и kd_tree
def testPointsInRect():
    tests = 10
    while (tests > 0):
        tests -= 1
        testPoints = generator.generateTestPoints()
        kdTree = kd_tree.buildKdTree(testPoints)
        rangeTree = range_tree.buildRangeTree(testPoints)
        rects = 10
        while (rects > 0):
            rects -= 1
            testRect = generator.generateTestRect()
            kdTreeResult = kd_tree.pointsInRectangle(kdTree, testRect)
            rangeTreeResult = range_tree.pointsInRectangle(rangeTree, testRect)
            if not structures.comparePointsLists(kdTreeResult, rangeTreeResult):
                print("\n------------------------- FAIL -------------------------\n")
                return
    print("\n------------------------- OK -------------------------\n")


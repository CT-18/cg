import structures
import generator
import range_tree
import kd_tree

# тестирование выполнения запроса в range-tree
def testRangeTreePointsInRect(testFunction):
    testPoints = generator.generateTestPoints()
    rangeTree = range_tree.buildRangeTree(testPoints)

    ok = True
    rects = 10
    while (rects > 0):
        rects -= 1
        testRect = generator.generateTestRect()

        result = testFunction(rangeTree, testRect)
        expectedResult = range_tree.pointsInRectangle(rangeTree, testRect)

        if not structures.comparePointsLists(expectedResult, result):
            ok = False
            rects = 0

    if ok:
        print("\n------------------------- OK -------------------------\n")
    else:
        print("\n------------------------- FAIL -------------------------\n")

# тестирование выполнения запроса в range-tree
def testKdTreePointsInRect(testFunction):
    testPoints = generator.generateTestPoints()
    kdTree = kd_tree.buildKdTree(testPoints)

    ok = True
    rects = 10
    while (rects > 0):
        rects -= 1
        testRect = generator.generateTestRect()

        result = testFunction(kdTree, testRect)
        expectedResult = kd_tree.pointsInRectangle(kdTree, testRect)

        if not structures.comparePointsLists(expectedResult, result):
            ok = False
            rects = 0

    if ok:
        print("\n------------------------- OK -------------------------\n")
    else:
        print("\n------------------------- FAIL -------------------------\n")

# тестирование данных реализаций range-tree и kd_tree
def testPointsInRect():
    testPoints = generator.generateTestPoints()
    testRect = generator.generateTestRect()
    kdTree = kd_tree.buildKdTree(testPoints)
    rangeTree = range_tree.buildRangeTree(testPoints)

    kdTreeResult = kd_tree.pointsInRectangle(kdTree, testRect)
    rangeTreeResult = range_tree.pointsInRectangle(rangeTree, testRect)

    if structures.comparePointsLists(kdTreeResult, rangeTreeResult):
        print("\n------------------------- OK -------------------------\n")
    else:
        print("\n------------------------- FAIL -------------------------\n")


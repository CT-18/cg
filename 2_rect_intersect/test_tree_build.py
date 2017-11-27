import generator
from structures import *

# тестирование построения kd-tree
def testBuildKdTree(testFunction):
    testBuildTree(testFunction, correctKdTreeStructure, correctKdTreeContent)

# тестирование построения range-tree
def testBuildRangeTree(testFunction):
    testBuildTree(testFunction, correctRangeTreeStructure, correctRangeTreeContent)

# вспомогательная функция для тестирования построения деревьев
def testBuildTree(testFunction, correctTreeStructure, correctTreeContent):
    for tests in range(0, 100):
        points = generator.generateTestPoints()
        result = testFunction(points)
        if (not correctTreeStructure(result)) or (not correctTreeContent(result, points)):
            print("\n------------------------- FAIL -------------------------\n")
            return
    print("\n------------------------- OK -------------------------\n")


# ------------------------- ПРОВЕРКА KD-TREE -------------------------

# проверка корректности структуры kd-tree
def correctKdTreeStructure(tree):
    return checkKdTreeStructure(tree.root, 0, 0, 0, False, False)

# вспомогательная рекурсивная функция для проверки структуры kd-tree
def checkKdTreeStructure(node, depth, grand, parent, haveLeftGrand, haveLeftParent):
    if node is None:
        return True
    if (node.leftChild is None) and (node.leftChild is None):
        pVal = node.point.x
        gVal = node.point.y
        if depth % 2 == 0:
            pVal, gVal = gVal, pVal
        if (haveLeftParent and (pVal < parent)) or ((not haveLeftParent) and (pVal > parent)):
            return False
        if (haveLeftGrand and (gVal < grand)) or ((not haveLeftGrand) and (gVal > grand)):
            return False
        return True
    if depth > 1:
        if haveLeftGrand and (node.med < grand):
            return False
        if (not haveLeftGrand) and (node.med > grand):
            return False
    if not (node.leftChild is None):
        if not checkKdTreeStructure(node.leftChild, depth + 1, parent, node.med, haveLeftParent, False):
            return False
    if not (node.rightChild is None):
        if not checkKdTreeStructure(node.rightChild, depth + 1, parent, node.med, haveLeftParent, True):
            return False
    return True

# проверка корректности данных, хранимых в kd-tree
def correctKdTreeContent(tree, points):
    treePoints = checkKdTreeContent(tree.root)
    return comparePointsLists(points, treePoints)

# возвращает список точек, хранящихся в kd-tree
def checkKdTreeContent(node):
    if node is None:
        return []
    if (node.leftChild is None) and (node.rightChild is None):
        return [node.point]
    result = []
    if not (node.leftChild is None):
        result.extend(checkKdTreeContent(node.leftChild))
    if not (node.rightChild is None):
        result.extend(checkKdTreeContent(node.rightChild))
    return result


# ------------------------- ПРОВЕРКА RANGE-TREE -------------------------

# проверка корректности структуры range-tree
def correctRangeTreeStructure(tree):
    return checkRangeTreeStructure(tree.root)

# вспомогательная рекурсивная функция для проверки структуры range-tree
def checkRangeTreeStructure(node):
    if node is None:
        return True
    if not (checkRangeTreeStructure(node.leftChild) and checkRangeTreeStructure(node.rightChild)):
        return False
    return ((node.leftChild is None) or (node.leftChild.value <= node.value)) and ((node.rightChild is None) or (node.rightChild.value > node.value))

# проверка корректности данных, хранимых в range-tree
def correctRangeTreeContent(tree, points):
    treePoints = checkRangeTreeContent(tree.root)
    return comparePointsLists(points, treePoints)

# возвращает список точек, хранящихся в range-tree
def checkRangeTreeContent(node):
    if node is None:
        return []
    if (node.leftChild is None) and (node.rightChild is None):
        return checkBinarySearchTreeContent(node.innerTree.root, node.innerTree.points)
    result = []
    result.extend(checkRangeTreeContent(node.leftChild))
    result.extend(checkRangeTreeContent(node.rightChild))
    return result

# возвращает список точек, хранящихся в binary-search-tree
def checkBinarySearchTreeContent(node, points):
    if node is None:
        return []
    result = []
    if (node.leftChild is None) and (node.rightChild is None):
        i = node.index
        border = node.index + node.length
        while i < border:
            result.append(points[i])
            i += 1
        return result
    result.extend(checkBinarySearchTreeContent(node.leftChild, points))
    result.extend(checkBinarySearchTreeContent(node.rightChild, points))
    return result
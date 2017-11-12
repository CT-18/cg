import generator
from structures import *

# тестирование построения kd-tree
def testBuildKdTree(testFunction):
    tests = 100
    while tests > 0:
        tests -= 1
        points = generator.generateTestPoints()
        result = testFunction(points)
        if (not correctKdTreeStructure(result)) or (not correctKdTreeContent(result, points)):
            print("\n------------------------- FAIL -------------------------\n")
            return
    print("\n------------------------- OK -------------------------\n")

# тестирование построения range-tree
def testBuildRangeTree(testFunction):
    tests = 100
    while (tests > 0):
        tests -= 1
        points = generator.generateTestPoints()
        result = testFunction(points)
        if (not correctRangeTreeStructure(result)) or (not correctRangeTreeContent(result, points)):
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
        for p in node.points:
            pVal = p.x
            gVal = p.y
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
        return node.points
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
def checkRangeTreeStructure(curNode):
    if curNode is None:
        return True
    if not (checkRangeTreeStructure(curNode.leftChild) and checkRangeTreeStructure(curNode.rightChild)):
        return False
    return ((curNode.leftChild is None) or (curNode.leftChild.value <= curNode.value)) and ((curNode.rightChild is None) or (curNode.rightChild.value > curNode.value))

# проверка корректности данных, хранимых в range-tree
def correctRangeTreeContent(tree, points):
    treePoints = checkRangeTreeContent(tree.root)
    return comparePointsLists(points, treePoints)

# возвращает список точек, хранящихся в range-tree
def checkRangeTreeContent(curNode):
    if curNode is None:
        return []
    if (curNode.leftChild is None) and (curNode.rightChild is None):
        return checkBinarySearchTreeContent(curNode.innerTree.root)
    result = []
    result.extend(checkRangeTreeContent(curNode.leftChild))
    result.extend(checkRangeTreeContent(curNode.rightChild))
    return result

# возвращает список точек, хранящихся в binary-search-tree
def checkBinarySearchTreeContent(curNode):
    if curNode is None:
        return []
    result = []
    result.extend(checkBinarySearchTreeContent(curNode.leftChild))
    result.append(curNode.point)
    result.extend(checkBinarySearchTreeContent(curNode.rightChild))
    return result
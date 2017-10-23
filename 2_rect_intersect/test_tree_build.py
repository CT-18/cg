import structures
import generator
import range_tree
import kd_tree

# тестирование построения range-tree
def testBuildRangeTree(testFunction):
    points = generator.generateTestPoints()

    result = testFunction(points)
    expectedResult = range_tree.buildRangeTree(points)

    if correctRangeTreeStructure(result) and compareRangeTrees(expectedResult, result):
        print("\n------------------------- OK -------------------------\n")
    else:
        print("\n------------------------- FAIL -------------------------\n")

# тестирование построения kd-tree
def testBuildKdTree(testFunction):
    points = generator.generateTestPoints()

    result = testFunction(points)

    if correctKdTreeStructure(result) and correctKdTreeContent(result, points):
        print("\n------------------------- OK -------------------------\n")
    else:
        print("\n------------------------- FAIL -------------------------\n")


# ------------------------- ПРОВЕРКА KD-TREE -------------------------

# проверка корректности структуры kd-tree
def correctKdTreeStructure(tree):
    return checkKdTreeStructure(tree.root, 0, 0, 0, False, False)

# вспомогательная рекурсивная функция для проверки структуры kd-tree
def checkKdTreeStructure(node, depth, grand, parent, haveLeftGrand, haveLeftParent):
    if node is None:
        return True
    if (node.leftChild is None) and (node.leftChild is None):
        pVal = node.x
        gVal = node.y
        if (depth % 2 == 0):
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
    treePoints = checkKdTreeContent([], tree.root)
    return structures.comparePointsLists(points, treePoints)

# возращает лист точек, хранящихся в kd-tree
def checkKdTreeContent(result, node):
    if node is None:
        return result
    if (node.leftChild is None) and (node.leftChild is None):
        result.append(structures.Point(node.x, node.y))
        return result
    if not (node.leftChild is None):
        checkKdTreeContent(result, node.leftChild)
    if not (node.rightChild is None):
        checkKdTreeContent(result, node.rightChild)
    return result

# ------------------------- ПРОВЕРКА RANGE-TREE -------------------------

# проверка корректности структуры range-tree
def correctRangeTreeStructure(tree):
    return checkRangeTreeStructure(tree.root)

# вспомогательная рекурсивная функция для проверки структуры range-tree
def checkRangeTreeStructure(curNode):
    if curNode is None:
        return True
    if (not (checkRangeTreeStructure(curNode.leftChild) and checkRangeTreeStructure(curNode.rightChild))):
        return False
    return ((curNode.leftChild is None) or (curNode.leftChild.value <= curNode.value)) and ((curNode.rightChild is None) or (curNode.rightChild.value > curNode.value))

# сравнение хранящихся в range-tree значений
def compareRangeTrees(first, second):
    first_nodes = findAll([], first.root)
    second_nodes = findAll([], second.root)
    if len(first_nodes) != len(second_nodes):
        return False
    s_it = iter(second_nodes)
    for f in first_nodes:
        s = s_it.__next__()
        if f.value != s.value:
            return False
        f_in_nodes = findAll([], f.innerTree.root)
        s_in_nodes = findAll([], s.innerTree.root)
        if len(f_in_nodes) != len(s_in_nodes):
            return False
        s_in_it = iter(s_in_nodes)
        for f_in in f_in_nodes:
            s_in = s_in_it.__next__()
            if f_in.value != s_in.value:
                return False
    return True

# добавляет в result все ноды из range-tree, упорядоченные по возрастанию value
def findAll(result, curNode):
    if curNode is None:
        return result
    findAll(result, curNode.leftChild)
    result.append(curNode)
    findAll(result, curNode.rightChild)
    return result


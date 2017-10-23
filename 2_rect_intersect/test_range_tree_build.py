import structures
import range_tree

from random import randint

TEST_SIZE = 100

# тестирование построения range-tree
def testBuildTree(testFunction):
    test = generateTest()

    result = testFunction(test)
    expectedResult = range_tree.buildRangeTree(test)

    if correctStructure(result) and compareTrees(expectedResult, result):
        print("\n------------------------- OK -------------------------\n")
    else:
        print("\n------------------------- FAIL -------------------------\n")

# генератор точек для теста
def generateTest():
    points = []
    for i in range(0, TEST_SIZE):
        points.append(structures.Point(randint(-10, 10), randint(-10, 10)))
    return points


# ------------------------- ПРОВЕРКИ -------------------------

# проверка корректности структуры
def correctStructure(tree):
    return checkStructure(tree.root)

# вспомогательная рекурсивная функция для проверки структуры
def checkStructure(curNode):
    if curNode is None:
        return True
    if (not (checkStructure(curNode.leftChild) and checkStructure(curNode.rightChild))):
        return False
    return ((curNode.leftChild is None) or (curNode.leftChild.value <= curNode.value)) and ((curNode.rightChild is None) or (curNode.rightChild.value > curNode.value))

# сравнение хранящихся в деревьях значений
def compareTrees(first, second):
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


from structures import *

class BinarySearchTreeNode:
    def __init__(self, value, point):
        self.leftChild = None
        self.rightChild = None
        self.value = value
        self.point = point

class BinarySearchTree:
    def __init__(self, points):
        self.root = None
        for p in points:
            if self.root is None:
                self.root = BinarySearchTreeNode(p.y, p)
            else:
                self.insertNode(self.root, BinarySearchTreeNode(p.y, p))

    def insertNode(self, curNode, newNode):
        if newNode.value <= curNode.value:
            if curNode.leftChild:
                self.insertNode(curNode.leftChild, newNode)
            else:
                curNode.leftChild = newNode
        else:
            if curNode.rightChild:
                self.insertNode(curNode.rightChild, newNode)
            else:
                curNode.rightChild = newNode

class Node:
    def __init__(self, value, innerTree):
        self.leftChild = None
        self.rightChild = None
        self.value = value
        self.innerTree = innerTree

class RangeTree:
    def __init__(self, root, vMin, vMax):
        self.root = root
        self.vMin = vMin
        self.vMax = vMax


# ------------------------- ПОСТРОЕНИЕ -------------------------

# функция построения range-tree
def buildRangeTree(points):
    return RangeTree(buildRangeTreeNode(points), min(points, key=keyX).x, max(points, key=keyX).x)

# функция построения ноды range-tree
def buildRangeTreeNode(points):
    if len(points) == 0:
        return None
    mediana = medianaX(points)
    pointsLeft = []
    pointsRight = []
    for p in points:
        if p.x <= mediana:
            pointsLeft.append(p)
        else:
            pointsRight.append(p)
    node = Node(mediana, BinarySearchTree(points))
    if (len(pointsLeft) == 0) or (len(pointsRight) == 0):
        return node
    node.leftChild = buildRangeTreeNode(pointsLeft)
    node.rightChild = buildRangeTreeNode(pointsRight)
    return node


# ------------------------- ВЫПОЛНЕНИЕ ЗАПРОСА -------------------------

# функция, возвращающая список точек, содержащихся в прямоугольнике rect
def pointsInRectangle(rangeTree, rect):
    result = []
    trees = getTrees(rangeTree.root, rangeTree.vMin, rangeTree.vMax, rect.xMin, rect.xMax)
    for tree in trees:
        result.extend(getPoints(tree.root, rect.yMin, rect.yMax))
    return result

# функция, возвращающая список binary-search-tree, хранящихся в тех нодах range-tree, value которых находится (нестрого) в интервале от vMin до vMax
def getTrees(curNode, curMin, curMax, vMin, vMax):
    if (curNode is None) or (vMin > vMax):
        return []
    result = []
    if (curNode.leftChild is None) and (curNode.rightChild is None):
        if (vMin <= curNode.value) and (curNode.value <= vMax):
            result.append(curNode.innerTree)
            return result
    if (vMin <= curMin) and (curMax <= vMax):
        result.append(curNode.innerTree)
        return result
    if vMin <= curNode.value:
        result.extend(getTrees(curNode.leftChild, curMin, curNode.value, vMin, min(curNode.value, vMax)))
    if vMax > curNode.value:
        result.extend(getTrees(curNode.rightChild, curNode.value, curMax, max(curNode.value, vMin), vMax))
    return result

# функция, возвращающая список точек, хранящихся в тех нодах binary-search-tree, value которых находится (нестрого) в интервале от vMin до vMax
def getPoints(curNode, vMin, vMax):
    if (curNode is None) or (vMin > vMax):
        return []
    result = []
    if curNode.value >= vMin:
        result.extend(getPoints(curNode.leftChild, vMin, vMax))
        if curNode.value <= vMax:
            result.append(curNode.point)
            result.extend(getPoints(curNode.rightChild, vMin, vMax))
    else:
        result.extend(getPoints(curNode.rightChild, vMin, vMax))
    return result







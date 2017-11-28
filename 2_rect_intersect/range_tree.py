from structures import *

class BSTNode:
    def __init__(self, value, index, length):
        self.leftChild = None
        self.rightChild = None
        self.value = value
        self.index = index
        self.length = length

class BinarySearchTree:
    def __init__(self, points, root, vMin, vMax):
        self.points = points
        self.root = root
        self.vMin = vMin
        self.vMax = vMax

class RTNode:
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
    points.sort(key=keyY)
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
    node = RTNode(mediana, buildBinarySearchTree(points))
    if (len(pointsLeft) == 0) or (len(pointsRight) == 0):
        return node
    node.leftChild = buildRangeTreeNode(pointsLeft)
    node.rightChild = buildRangeTreeNode(pointsRight)
    return node

# функция построения binary-search-tree (вложенного в range-tree дерева)
def buildBinarySearchTree(points):
    return BinarySearchTree(points, buildBinarySearchTreeNode(0, len(points), points), points[0].y, points[len(points) - 1].y)

# функция построения ноды binary-search-tree
def buildBinarySearchTreeNode(index, length, points):
    if (len(points) == 0):
        return None
    mediana = points[index + (length - 1) // 2].y
    lengthLeft = length // 2
    lengthRight = length - lengthLeft
    node = BSTNode(mediana, index, length)
    if (lengthLeft == 0) or (lengthRight == 0):
        return node
    node.leftChild = buildBinarySearchTreeNode(index, lengthLeft, points)
    node.rightChild = buildBinarySearchTreeNode(index + lengthLeft, lengthRight, points)
    return node


# ------------------------- ВЫПОЛНЕНИЕ ЗАПРОСА -------------------------

# функция, возвращающая список точек, содержащихся в прямоугольнике rect
def pointsInRectangle(rangeTree, rect):
    result = []
    trees = getTrees(rangeTree.root, rangeTree.vMin, rangeTree.vMax, rect.xMin, rect.xMax)
    for tree in trees:
        result.extend(getPoints(tree.root, tree.points, tree.vMin, tree.vMax, rect.yMin, rect.yMax))
    return result

# функция, возвращающая список binary-search-tree, содержаших в объединении все точки, x координата которых находится (нестрого) в интервале от vMin до vMax
def getTrees(node, curMin, curMax, vMin, vMax):
    if (node is None) or (vMin > vMax):
        return []
    result = []
    if (node.leftChild is None) and (node.rightChild is None):
        if (vMin <= node.value) and (node.value <= vMax):
            result.append(node.innerTree)
            return result
    if (vMin <= curMin) and (curMax <= vMax):
        result.append(node.innerTree)
        return result
    if vMin <= node.value:
        result.extend(getTrees(node.leftChild, curMin, node.value, vMin, min(node.value, vMax)))
    if vMax > node.value:
        result.extend(getTrees(node.rightChild, node.value, curMax, max(node.value, vMin), vMax))
    return result

# функция, возвращающая список точек, y координата которых находится (нестрого) в интервале от vMin до vMax
def getPoints(node, points, curMin, curMax, vMin, vMax):
    if (node is None) or (vMin > vMax):
        return []
    result = []
    if (node.leftChild is None) and (node.rightChild is None):
        if (vMin <= node.value) and (node.value <= vMax):
            return getPointsFromNode(node, points)
    if (vMin <= curMin) and (curMax <= vMax):
        return getPointsFromNode(node, points)
    if vMin <= node.value:
        result.extend(getPoints(node.leftChild, points, curMin, node.value, vMin, min(node.value, vMax)))
    if vMax >= node.value:
        result.extend(getPoints(node.rightChild, points, node.value, curMax, max(node.value, vMin), vMax))
    return result

# функция, возвращающая список всех точек, за которые отвечает данная нода
def getPointsFromNode(node, points):
    result = []
    i = node.index
    border = node.index + node.length
    for i in range(node.index, border):
        result.append(points[i])
    return result
import structures

class Node:
    def __init__(self, value, innerTree):
        self.leftChild = None
        self.rightChild = None
        self.innerTree = innerTree
        self.value = value

class RangeTree:
    def __init__(self):
        self.root = None

    def setRoot(self, newRoot):
        self.root = newRoot

    def insert(self, value, innerTree):
        if (self.root is None):
            self.setRoot(Node(value, innerTree))
        else:
            self.insertNode(self.root, Node(value, innerTree))

    def insertNode(self, curNode, newNode):
        if (newNode.value <= curNode.value):
            if (curNode.leftChild):
                self.insertNode(curNode.leftChild, newNode)
            else:
                curNode.leftChild = newNode
        else:
            if (curNode.rightChild):
                self.insertNode(curNode.rightChild, newNode)
            else:
                curNode.rightChild = newNode


# ------------------------- ПОСТРОЕНИЕ -------------------------

# функция построения range-tree
def buildRangeTree(points):
    orderedPoints = {}
    xValues = []

    for p in points:
        if xValues.count(p.x) == 0:
            orderedPoints[p.x] = []
            xValues.append(p.x)
        orderedPoints[p.x].append(p.y)

    resultTree = RangeTree()
    for x in xValues:
        innerTree = RangeTree()
        for y in orderedPoints[x]:
            innerTree.insert(y, None)
        resultTree.insert(x, innerTree)

    return resultTree


# ------------------------- ВЫПОЛНЕНИЕ ЗАПРОСА -------------------------

# вспомогательная функция для getNodes
def findInterval(result, curNode, vMin, vMax):
    if (curNode in None or vMin > vMax):
        return result
    if curNode.value >= vMin:
        if curNode.value <= vMax:
            findInterval(result, curNode.leftChild, vMin, vMax)
            result.append(curNode)
            findInterval(result, curNode.rightChild, vMin, vMax)
        else:
            findInterval(result, curNode.leftChild, vMin, vMax)
    else:
        findInterval(result, curNode.rightChild, vMin, vMax)
    return result

# функция, возвращающая лист нод range-tree, value которых находится (нестрого) в интервале от vMin до vMax
def getNodes(rangeTree, vMin, vMax):
    return findInterval([], rangeTree.root, vMin, vMax)

# функция, возвращающая лист точек, содержащихся в прямоугольнике rect
def pointsInRectangular(rangeTree, rect):
    result = []
    yTrees = getNodes(rangeTree, rect.xMin, rect.xMax)
    for yTree in yTrees:
        yNodes = getNodes(yTree.innerTree, rect.yMin, rect.yMax)
        for yNode in yNodes:
            result.append(structures.Point(yTree.value, yNode.value))
    return result




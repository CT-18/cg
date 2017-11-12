from structures import *

class Node:
    def __init__(self, points):
        self.leftChild = None
        self.rightChild = None
        self.points = points
        self.med = 0

    def setMedian(self, med):
        self.med = med

class KdTree:
    def __init__(self, root, xMin, yMin, xMax, yMax):
        self.root = root
        self.xMin = xMin
        self.yMin = yMin
        self.xMax = xMax
        self.yMax = yMax


# ------------------------- ПОСТРОЕНИЕ -------------------------

# функция построения kd-tree
def buildKdTree(points):
    if len(points) == 0:
        return KdTree(None, 0, 0, 0, 0)

    root = buildKdNode(points, False)

    xMin = min(points, key=keyX).x
    xMax = max(points, key=keyX).x
    yMin = min(points, key=keyY).y
    yMax = max(points, key=keyY).y

    return KdTree(root, xMin, yMin, xMax, yMax)

# вспомогательная функция для kd-tree
def buildKdNode(points, depth):
    if len(points) == 0:
        return None
    node = Node(points)
    if len(points) == 1:
        return node
    pointsLeft = []
    pointsRight = []
    if not depth:
        # четная глубина - делим вертикальной прямой
        mediana = medianaX(points)
        for p in points:
            if p.x <= mediana:
                pointsLeft.append(p)
            else:
                pointsRight.append(p)
    else:
        # нечетная глубина - делим горизонтальной прямой
        mediana = medianaY(points)
        for p in points:
            if p.y <= mediana:
                pointsLeft.append(p)
            else:
                pointsRight.append(p)

    node.setMedian(mediana)
    if len(pointsLeft) > 0:
        node.leftChild = buildKdNode(pointsLeft, not depth)
    if len(pointsRight) > 0:
        node.rightChild = buildKdNode(pointsRight, not depth)
    return node


# ------------------------- ВЫПОЛНЕНИЕ ЗАПРОСА -------------------------

# функция, возвращающая список точек, содержащихся в прямоугольнике rect
def pointsInRectangle(kdTree, rect):
    region = Rectangle(kdTree.xMin, kdTree.yMin, kdTree.xMax, kdTree.yMax)
    return getPoints(kdTree.root, False, region, rect)

# вспомогательная функция для pointInRectangle
def getPoints(node, depth, region, rect):
    if node is None:
        return []
    result = []

    if (node.leftChild is None) and (node.rightChild is None):
        if (rect.xMin <= node.points[0].x) and (rect.xMax >= node.points[0].x) and (rect.yMin <= node.points[0].y) and (rect.yMax >= node.points[0].y):
            result.extend(node.points)
        return result

    if rect.include(region):
        result.extend(node.points)
        return result

    if not depth:
        # хранится вертикальная прямая (медиана по х)
        if (region.yMin > rect.yMax) or (region.yMax < rect.yMin):
            return result
        if node.med < rect.xMax:
            result.extend(getPoints(node.rightChild, not depth, Rectangle(node.med, region.yMin, region.xMax, region.yMax), rect))
        if node.med >= rect.xMin:
            result.extend(getPoints(node.leftChild, not depth, Rectangle(region.xMin, region.yMin, node.med, region.yMax), rect))
    else:
        # хранится горизонтальная прямая (медиана по y)
        if (region.xMin > rect.xMax) or (region.xMax < rect.xMin):
            return result
        if node.med < rect.yMax:
            result.extend(getPoints(node.rightChild, not depth, Rectangle(region.xMin, node.med, region.xMax, region.yMax), rect))
        if node.med >= rect.yMin:
            result.extend(getPoints(node.leftChild, not depth, Rectangle(region.xMin, region.yMin, region.xMax, node.med), rect))
    return result
import copy
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

    points.sort(key=keyX)
    sortX = copy.deepcopy(points)
    points.sort(key=keyY)
    sortY = copy.deepcopy(points)

    root = buildKdNode(sortX, sortY, False)
    xMin = sortX[0].x
    xMax = sortX[len(sortX) - 1].x
    yMin = sortY[0].y
    yMax = sortY[len(sortY) - 1].y
    return KdTree(root, xMin, yMin, xMax, yMax)

# вспомогательная функция для kd-tree
def buildKdNode(pSortX, pSortY, depth):
    if len(pSortX) == 0:
        return None
    node = Node(pSortX)
    if len(pSortX) == 1:
        return node
    mediana = 0
    pSortLeftX = []
    pSortRightX = []
    pSortLeftY = []
    pSortRightY = []
    if not depth:
        # четная глубина - делим вертикальной прямой
        mediana = pSortX[(len(pSortX) - 1) // 2].x
        inLeft = True
        equalMedLeftY = set()
        for p in pSortX:
            if p.x < mediana:
                pSortLeftX.append(p)
            else:
                if p.x == mediana:
                    if inLeft:
                        equalMedLeftY.add(p.y)
                        pSortLeftX.append(p)
                    else:
                        pSortRightX.append(p)
                    inLeft = not inLeft
                else:
                    pSortRightX.append(p)

        for p in pSortY:
            if p.x < mediana:
                pSortLeftY.append(p)
            else:
                if p.x == mediana:
                    if p.y in equalMedLeftY:
                        pSortLeftY.append(p)
                    else:
                        pSortRightY.append(p)
                else:
                    pSortRightY.append(p)
    else:
        # нечетная глубина - делим горизонтальной прямой
        mediana = pSortY[(len(pSortY) - 1) // 2].y
        inLeft = True
        equalMedLeftX = set()
        for p in pSortX:
            if p.y < mediana:
                pSortLeftX.append(p)
            else:
                if p.y == mediana:
                    if inLeft:
                        equalMedLeftX.add(p.x)
                        pSortLeftX.append(p)
                    else:
                        pSortRightX.append(p)
                    inLeft = not inLeft
                else:
                    pSortRightX.append(p)

        for p in pSortY:
            if p.y < mediana:
                pSortLeftY.append(p)
            else:
                if p.y == mediana:
                    if p.x in equalMedLeftX:
                        pSortLeftY.append(p)
                    else:
                        pSortRightY.append(p)
                else:
                    pSortRightY.append(p)
    node.setMedian(mediana)
    if len(pSortLeftX) > 0:
        node.leftChild = buildKdNode(pSortLeftX, pSortLeftY, not depth)
    if len(pSortLeftY) > 0:
        node.rightChild = buildKdNode(pSortRightX, pSortRightY, not depth)
    return node


# ------------------------- ВЫПОЛНЕНИЕ ЗАПРОСА -------------------------

# функция, возвращающая лист точек, содержащихся в прямоугольнике rect
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
        if node.med <= rect.xMax:
            result.extend(getPoints(node.rightChild, not depth, Rectangle(node.med, region.yMin, region.xMax, region.yMax), rect))
        if node.med >= rect.xMin:
            result.extend(getPoints(node.leftChild, not depth, Rectangle(region.xMin, region.yMin, node.med, region.yMax), rect))
    else:
        # хранится горизонтальная прямая (медиана по y)
        if (region.xMin > rect.xMax) or (region.xMax < rect.xMin):
            return result
        if node.med <= rect.yMax:
            result.extend(getPoints(node.rightChild, not depth, Rectangle(region.xMin, node.med, region.xMax, region.yMax), rect))
        if node.med >= rect.yMin:
            result.extend(getPoints(node.leftChild, not depth, Rectangle(region.xMin, region.yMin, region.xMax, node.med), rect))
    return result
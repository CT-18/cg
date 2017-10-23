import structures
import copy

class Node:
    def __init__(self):
        self.leftChild = None
        self.rightChild = None
        self.med = 0
        self.x = 0
        self.y = 0

    def setMedian(self, med):
        self.med = med

    def setPoint(self, x, y):
        self.x = x
        self.y = y

class KdTree:
    def __init__(self, root, xMin, xMax, yMin, yMax):
        self.root = root
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax


# ------------------------- ПОСТРОЕНИЕ -------------------------

# функция построения kd-tree
def buildKdTree(points):
    if (len(points) == 0):
        return KdTree(None, 0, 0, 0, 0)

    points.sort(key=structures.keyX)
    sortX = copy.deepcopy(points)
    points.sort(key=structures.keyY)
    sortY = copy.deepcopy(points)

    root = buildKdNode(sortX, sortY, False)
    xMin = sortX[0].x - 1
    xMax = sortX[len(sortX) - 1].x + 1
    yMin = sortY[0].y - 1
    yMax = sortY[len(sortY) - 1].y + 1
    return KdTree(root, xMin, xMax, yMin, yMax)

# вспомогательная функция для kd-tree
def buildKdNode(pSortX, pSortY, depth):
    if (len(pSortX) == 0):
        return None
    node = Node()
    if (len(pSortX) == 1):
        node.setPoint(pSortX[0].x, pSortX[0].y)
        return node
    mediana = 0
    pSortLeftX = []
    pSortRightX = []
    pSortLeftY = []
    pSortRightY = []
    if not depth:
        # четная глубина - делим вертикальной прямой
        mediana = pSortX[(len(pSortX) - 1) // 2].x
        repeat = 2
        while (repeat > 0):
            repeat -= 1
            for p in pSortX:
                if p.x <= mediana:
                    pSortLeftX.append(p)
                else:
                    pSortRightX.append(p)
            if len(pSortLeftX) - len(pSortRightX) > 3:
                mediana -= 1
                pSortLeftX.clear()
                pSortRightX.clear()
            else:
                repeat -=1
        for p in pSortY:
            if p.x <= mediana:
                pSortLeftY.append(p)
            else:
                pSortRightY.append(p)
    else:
        # нечетная глубина - делим горизонтальной прямой
        mediana = pSortY[(len(pSortY) - 1) // 2].y
        repeat = 2
        while (repeat > 0):
            repeat -= 1
            for p in pSortX:
                if p.y <= mediana:
                    pSortLeftX.append(p)
                else:
                    pSortRightX.append(p)
            if len(pSortLeftX) - len(pSortRightX) > 2:
                mediana -= 1
                pSortLeftX.clear()
                pSortRightX.clear()
            else:
                repeat -= 1
        for p in pSortY:
            if p.y <= mediana:
                pSortLeftY.append(p)
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
    region = structures.Rectangle(kdTree.xMin, kdTree.xMax, kdTree.yMin, kdTree.yMax)
    return getPoints([], kdTree.root, False, region, rect)

# вспомогательная функция для pointInRectangle
def getPoints(result, node, depth, region, rect):
    if (node is None):
        return result

    if (node.leftChild is None) and (node.rightChild is None):
        if (rect.xMin <= node.x) and (rect.xMax >= node.x) and (rect.yMin <= node.y) and (rect.yMax >= node.y):
            result.append(structures.Point(node.x, node.y))
        return result

    newRegion = structures.Rectangle(region.xMin, region.xMax, region.yMin, region.yMax)

    if not depth:
        # хранится вертикальная прямая (медиана по х)
        if (region.yMin >= rect.yMax) or (region.yMax < rect.yMin):
            return result

        if (node.med < rect.xMax):
            newRegion.xMin = node.med
            getPoints(result, node.rightChild, not depth, newRegion, rect)
        if (node.med >= rect.xMin):
            newRegion.xMax = node.med
            getPoints(result, node.leftChild, not depth, newRegion, rect)

    else:
        # хранится горизонтальная прямая (медиана по y)
        if (region.xMin >= rect.xMax) or (region.xMax < rect.xMin):
            return result

        if (node.med < rect.yMax):
            newRegion.yMin = node.med
            getPoints(result, node.rightChild, not depth, newRegion, rect)
        if (node.med >= rect.yMin):
            newRegion.yMax = node.med
            getPoints(result, node.leftChild, not depth, newRegion, rect)

    return result

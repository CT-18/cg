import numpy as np
from numpy import *
from enum import Enum

class Segment:
    "Структура, описывающая отрезок"
    
    def __init__(self, p, q):
        # Предполагаем, что p и q упорядочены лексикографически"
        self.p = p #Левая точка
        self.q = q #Правая точка
    
    def __repr__(self):
        return str(self.p) + ', ' + str(self.q)


class Trapezoid:
    "Структура, описывающая трапецоид"
    
    def __init__(self, top, bottom, leftp, rightp):
        # Верхний и нижний отрезки
        self.top = top
        self.bottom = bottom
        
        # Левая и правая точки
        self.leftp = leftp
        self.rightp = rightp
        
        # Соседи трапецоида
        self.leftnb = [None, None]
        self.rightnb = [None, None]
        
        # Ссылки на TrapezoidNode
        self.node = None
     
    def isMostRight(self):
        return (self.rightp == None)
    
    def isMostLeft(self):
        return (self.leftp == None)


class AbstractNode:
    "Структура, описывающая узел локализационной структуры"
    
    def __init__(self, left = None, right = None):
        self.left = left
        self.right = right
    
    def visit(self, q):
        pass

class XNode(AbstractNode):
    
    def __init__(self, point, left, right):
        AbstractNode.__init__(self, left, right)
        self.point = point

    def visit(self, point):
        # TODO: лексикографическое сравнение точек взять из общей библиотеки
        if point[0] < self.point[0]:
            return self.left.visit(point)
        elif point[0] > self.point[0]:
            return self.right.visit(point)
        else: # x-координаты равны
            if point[1] < self.point[1]:
                return self.left.visit(point)
            elif point[1] > self.point[1]:
                return self.right.visit(point)
            else:
                return self.left.visit(point) + self.right.visit(point)


class YNode(AbstractNode):
    
    def __init__(self, segment, left, right):
        AbstractNode.__init__(self, left, right)
        self.segment = segment

    def visit(self, point):
        # TODO: предикат поворота взять из общей библиотеки
        turn = np.sign(np.linalg.det(np.array([self.segment.p, self.segment.q]) - point))
        if turn == -1:
            return self.right.visit(point)
        elif turn == 1:
            return self.left.visit(point)
        else:
            return self.left.visit(point) + self.right.visit(point)


class TrapezoidNode(AbstractNode):
    
    def __init__(self, trapezoid):
        AbstractNode.__init__(self)
        self.tr = trapezoid
        trapezoid.node = self
        self.links = []

    def visit(self, point):
        return [self.tr]


def intersectSegment(s, leftTr):
    "Возвращает список трапецоидов, которые пересекает отрезок"
    while not leftTr.isMostRight():
        # Поиск остановится, если у трапецоида отсутствует правый вертикальный отрезок или нету соседей.
        # TODO: лексикографическое сравнение точек взять из общей библиотеки
        if s.q[0] < leftTr.rightp[0]:
            break
        elif s.q[0] == leftTr.rightp[0]:
            if s.q[1] <= leftTr.rightp[1]:
                break
            else:
                leftTr = leftTr.rightnb[0]
                assert leftTr != None
                yield leftTr
        else:
            # Иначе считаем поворот точки rightp относительно прямой s
            # TODO: предикат поворота взять из общей библиотеки
            sign = np.sign(np.linalg.det(np.array([s.p, s.q]) - leftTr.rightp))
            if sign == 1:
                # Отрезок пересекает нижнего соседа
                leftTr = leftTr.rightnb[1]
            elif sign == -1:
                # Отрезок пересекает верхнего соседа
                leftTr = leftTr.rightnb[0]
            else: #sign == 0
                # Отрезок касается вершины, по y-координате ясно, вниз или вверх пойдёт отрезок
                leftTr = leftTr.rightnb[0 if (s.q[1] < s.p[1]) else 1]
            assert leftTr != None
            yield leftTr


class TrapezoidalMap():
    
    def __init__(self):
        "Список всех трапецоидов, для отрисовки"
        self.tr = [Trapezoid(None, None, None, None)]
        self.segments = []
        "Корень поисковой структуры"
        self.root = TrapezoidNode(self.tr[0])
        self.tr[0].link = self.root
    
    def localize(self, q):
        "Возвращает список трапецоидов, в которые попала точка"
        return self.root.visit(q)
        
    def __insertInside(self, s, parent):
        "Метод для вставки отрезка, попавшего целиком в трапецоид"
        # Создаем 4 новых трапецоида
        up = Trapezoid(parent.top, s, s.p, s.q)
        down = Trapezoid(s, parent.bottom, s.p, s.q)
        left = Trapezoid(parent.top, parent.bottom, parent.leftp, s.p)
        right = Trapezoid(parent.top, parent.bottom, s.q, parent.rightp)
        # Запоминаем их
        self.tr.append(up)
        self.tr.append(down)
        self.tr.append(left)
        self.tr.append(right)
        # Расставляем соседей
        up.leftnb = [left, None]
        up.rightnb = [right, None]
        down.leftnb = [None, left]
        down.rightnb = [None, right]
        left.leftnb = parent.leftnb
        left.rightnb = [up, down]
        right.rightnb = parent.rightnb
        right.leftnb = [up, down]
        #У соседей parent-a теперь новые трапецоиды
        for i in range(2):
            if parent.leftnb[i] != None:
                for j in range(2): # реально надо только 1 соседа справа обновить, но так кода меньше
                    if parent.leftnb[i].rightnb[j] == parent:
                        parent.leftnb[i].rightnb[j] = left
            if parent.rightnb[i] != None: # не копипаста
                for j in range(2):
                    if parent.rightnb[i].leftnb[j] == parent:
                        parent.rightnb[i].leftnb[j] = right
        # Строим новое поддерево"
        upNode = TrapezoidNode(up)
        downNode = TrapezoidNode(down)
        leftNode = TrapezoidNode(left)
        rightNode = TrapezoidNode(right)
        segmentNode = YNode(s, upNode, downNode)
        qNode = XNode(s.q, segmentNode, rightNode)
        pNode = XNode(s.p, leftNode, qNode)
        # Обновим ссылки между узлами и трапецоидами
        upNode.links.append(segmentNode)
        downNode.links.append(segmentNode)
        leftNode.links.append(pNode)
        rightNode.links.append(qNode)
        for ancestor in parent.node.links:
            if ancestor.left == parent.node:
                ancestor.left = pNode
            elif ancestor.right == parent.node:
                ancestor.right = pNode
            else:
                raise Exception('Error')
        # Удалим старый трапецоид
        self.tr.remove(parent)
        # Обновим корень, если это первое добавление
        if type(self.root) == type(upNode):
            self.root = pNode
    
    def __leftInsert(self, s, parent):
        "Метод для вставки отрезка в самый левый трапецоид. Отрезок пересекает как минимум 2 трапецоида!"
        # TODO: сравнить левые точки лексикографически, может и не надо создавать
        assert s.p != parent.rightp # отрезок не должен был попасть в этот трапецоид
        up = Trapezoid(parent.top, s, s.p, parent.rightp)
        down = Trapezoid(s, parent.bottom, s.p, parent.rightp) # одна из rightp ещё не известна
        left = Trapezoid(parent.top, parent.bottom, parent.leftp, s.p)
        self.tr.append(up)
        self.tr.append(down)
        self.tr.append(left)
        up.leftnb = [left, None]
        down.leftnb = [None, left]
        left.leftnb = parent.leftnb
        left.rightnb = [up, down]
        for i in range(2):
            if parent.leftnb[i] != None:
                for j in range(2): # реально надо только 1 соседа справа обновить, но так кода меньше
                    if parent.leftnb[i].rightnb[j] == parent:
                        parent.leftnb[i].rightnb[j] = left
        # TODO: предикат поворота взять из общей библиотеки
        sign = np.sign(np.linalg.det(np.array([s.p, s.q]) - parent.rightp))
        if sign == 1:
            # точка выше отрезка, нижний трапецоид не закончен
            down.rightp = None
            up.rightnb = [parent.rightnb[0], None] # нижний не известен
            if parent.rightnb[0] != None:
                for i in range(2):
                    if parent.rightnb[0].leftnb[i] == parent:
                        parent.rightnb[0].leftnb[i] = up
        elif sign == -1:
            # точка ниже отрезка, верхний трапецоид не закончен
            up.rightp = None
            down.rightnb = [None, parent.rightnb[1]]
            if parent.rightnb[1] != None:
                for i in range(2):
                    if parent.rightnb[1].leftnb[i] == parent:
                        parent.rightnb[1].leftnb[i] = down
        else:
            # внезапно, в первом трапецоиде отрезок попал в его правую вершину.
            # а такого не должно было быть, т.к. либо отрезок пересек 1 трапецоид,
            # либо два отрезка имеют внутреннее пересечение
            raise Exception('Error')
        # Строим новое поддерево
        upNode = TrapezoidNode(up)
        downNode = TrapezoidNode(down)
        leftNode = TrapezoidNode(left)
        segmentNode = YNode(s, upNode, downNode)
        pNode = XNode(s.p, leftNode, segmentNode)
        # Обновим ссылки между узлами и трапецоидами
        upNode.links.append(segmentNode)
        downNode.links.append(segmentNode)
        leftNode.links.append(pNode)
        for ancestor in parent.node.links:
            if ancestor.left == parent.node:
                ancestor.left = pNode
            elif ancestor.right == parent.node:
                ancestor.right = pNode
            else:
                raise Exception('Error')
        self.tr.remove(parent)
        return [up, down] # будем возвращать сначала верхний, а затем нижний
    
    def __segmentInsert(self, s, parent, leftNb):
        "Вставка отрезка в очередной трапецоид, возможно последний"
        # создаем лишь 1 новый трапецоид, т.к. второй был незакончен на прошлом шаге
        # недоделан либо верхний, либо нижний. определим это по его левым соседям
        if leftNb[0].rightp == None:
            assert parent.leftp == leftNb[1].rightp, str(parent.leftp) + str(leftNb[1].rightp)
            # новый трапецоид - нижний; верхний продолжается
            up = leftNb[0]
            down = Trapezoid(s, parent.bottom, parent.leftp, parent.rightp)
            self.tr.append(down)
            leftNb[1].rightnb[0] = down
            down.leftnb = [leftNb[1], parent.leftnb[1]]
            if parent.leftnb[1] != None:
                for j in range(2): # реально надо только 1 соседа справа обновить, но так кода меньше
                    if parent.leftnb[1].rightnb[j] == parent:
                        parent.leftnb[1].rightnb[j] = down
            upNode = up.node
            downNode = TrapezoidNode(down)
        else:
            assert parent.leftp == leftNb[0].rightp, str(parent.leftp) + str(leftNb[0].rightp)
            # новый трапецоид - верхний, а нижний продолжается
            down = leftNb[1]
            up = Trapezoid(parent.top, s, parent.leftp, parent.rightp)
            self.tr.append(up)
            leftNb[0].rightnb[1] = up
            up.leftnb = [parent.leftnb[0], leftNb[0]]
            if parent.leftnb[0] != None:
                for j in range(2): # реально надо только 1 соседа справа обновить, но так кода меньше
                    if parent.leftnb[0].rightnb[j] == parent:
                        parent.leftnb[0].rightnb[j] = up
            upNode = TrapezoidNode(up)
            downNode = down.node
        # Надо понять, верхний или нижний трапецоид продлевать
        # TODO: предикат поворота взять из общей библиотеки
        sign = np.sign(np.linalg.det(np.array([s.p, s.q]) - parent.rightp))
        if sign == 1:
            # точка выше отрезка, нижний трапецоид не закончен
            down.rightp = None
            up.rightp = parent.rightp # если в прошлый раз не закончили его
            up.rightnb = [parent.rightnb[0], None]
            if parent.rightnb[0] != None:
                for i in range(2):
                    if parent.rightnb[0].leftnb[i] == parent:
                        parent.rightnb[0].leftnb[i] = up
        elif sign == -1:
            # точка ниже отрезка, верхний трапецоид не закончен
            up.rightp = None
            down.rightp = parent.rightp # если в прошлый раз не закончили его
            down.rightnb = [None, parent.rightnb[1]]
            if parent.rightnb[1] != None:
                for i in range(2):
                    if parent.rightnb[1].leftnb[i] == parent:
                        parent.rightnb[1].leftnb[i] = down
        else:
            # отрезок попал в вершину, значит это последний трапецоид
            up.rightnb = [parent.rightnb[0], None]
            down.rightnb = [None, parent.rightnb[1]]
            up.rightp = parent.rightp
            down.rightp = parent.rightp
        #TODO
        segmentNode = YNode(s, upNode, downNode)
        upNode.links.append(segmentNode)
        downNode.links.append(segmentNode)
        for ancestor in parent.node.links:
            if ancestor.left == parent.node:
                ancestor.left = segmentNode
            elif ancestor.right == parent.node:
                ancestor.right = segmentNode
            else:
                raise Exception('Error')
        self.tr.remove(parent)
        return [up, down]
    
    def __rightInsert(self, s, parent, leftNb):
        "Вставка отрезка в последний трапецоид"
        # TODO: сравнить левые точки лексикографически, может и не надо создавать
        assert s.q != parent.leftp # отрезок не должен был попасть в этот трапецоид
        # TODO: предикат поворота взять из общей библиотеки
        sign = 1 if parent.isMostRight() else np.sign(np.linalg.det(np.array([s.p, s.q]) - parent.rightp))
        if sign == 0:
            # правый конец отрезка попал в вершину, значит это последний трапецоид
            assert s.q == parent.rightp
            leftNb = self.segmentInsert(s, parent, leftNb)
            if parent.rightnb[0] != None:
                assert parent.rightnb[0].leftnb[0] == parent
                parent.rightnb[0].leftnb[0] = leftNb[0]
            if parent.rightnb[1] != None:
                assert parent.rightnb[1].leftnb[1] == parent
                parent.rightnb[1].leftnb[1] = leftNb[1]
            return
        if leftNb[0].rightp == None:
            assert parent.leftp == leftNb[1].rightp, str(parent.leftp) + str(leftNb[1].rightp)
            # новый трапецоид - нижний; верхний продолжается
            up = leftNb[0]
            up.rightp = s.q
            down = Trapezoid(s, parent.bottom, parent.leftp, s.q)
            self.tr.append(down)
            leftNb[1].rightnb[0] = down
            down.leftnb = [leftNb[1], parent.leftnb[1]]
            if parent.leftnb[1] != None:
                for j in range(2): # реально надо только 1 соседа справа обновить, но так кода меньше
                    if parent.leftnb[1].rightnb[j] == parent:
                        parent.leftnb[1].rightnb[j] = down
            upNode = up.node
            downNode = TrapezoidNode(down)
        else:
            assert parent.leftp == leftNb[0].rightp, str(parent.leftp) + str(leftNb[0].rightp)
            # новый трапецоид - верхний, а нижний продолжается
            down = leftNb[1]
            down.rightp = s.q
            up = Trapezoid(parent.top, s, parent.leftp, s.q)
            self.tr.append(up)
            leftNb[0].rightnb[1] = up
            up.leftnb = [parent.leftnb[0], leftNb[0]]
            if parent.leftnb[0] != None:
                for j in range(2): # реально надо только 1 соседа справа обновить, но так кода меньше
                    if parent.leftnb[0].rightnb[j] == parent:
                        parent.leftnb[0].rightnb[j] = up
            upNode = TrapezoidNode(up)
            downNode = down.node
        right = Trapezoid(parent.top, parent.bottom, s.q, parent.rightp)
        self.tr.append(right)
        right.leftnb = [up, down]
        up.rightnb = [right, None]
        down.rightnb = [None, right]
        right.rightnb = parent.rightnb
        for i in range(2):
            if parent.rightnb[i] != None:
                for j in range(2):# реально надо только 1 соседа справа обновить, но так кода меньше
                    if parent.rightnb[i].leftnb[j] == parent:
                        parent.rightnb[i].leftnb[j] = right
        # Строим новое поддерево
        rightNode = TrapezoidNode(right)
        segmentNode = YNode(s, upNode, downNode)
        qNode = XNode(s.q, segmentNode, rightNode)
        # Обновим ссылки между узлами и трапецоидами
        upNode.links.append(segmentNode)
        downNode.links.append(segmentNode)
        rightNode.links.append(qNode)
        for ancestor in parent.node.links:
            if ancestor.left == parent.node:
                ancestor.left = qNode
            elif ancestor.right == parent.node:
                ancestor.right = qNode
            else:
                raise Exception('Error')
        self.tr.remove(parent)
        return # ну типо конец
    
    def insert(self, s):
        "Вставка отрезка в трапецоидную карту"
        self.segments.append(s)
        # локализуем первую точку
        localizedList = self.localize(s.p)
        firstTr = None
        if len(localizedList) == 1:
            # Левая вершина отрезка не попала на вершину другого отерзка
            firstTr = localizedList[0]
            # TODO: лексикографическое сравнение точек взять из общей библиотеки
            if firstTr.isMostLeft() or s.p[0] > firstTr.leftp[0] or (s.p[0] == firstTr.leftp[0] and s.p[1] > firstTr.leftp[1]):
                if firstTr.isMostRight() or s.q[0] < firstTr.rightp[0] or s.q[0] == firstTr.rightp[0] and s.q[1] < firstTr.rightp[1]:
                    # Простой случай: вставка отрезка целиком в один трапецоид
                    self.__insertInside(s, firstTr)
                    return
            # Вставим отрезок в самый левый трапецоид
            trNodes = self.__leftInsert(s, firstTr)
        else:
            # Левая вершина отрезка попала на вершину другого отерзка
            # Надо выбрать тот трапецоид, в котором идёт отрезок.
            tempList = []
            for tr in localizedList:
                if tr.leftp == s.p: # Не нужны трапецоиды, у которых вершина отрезка правая
                    tempList.append(tr)
            localizedList = tempList
            assert len(localizedList) > 0
            if len(localizedList) == 1: # Вдруг нашли)
                firstTr = localizedList[0]
            else:
                # Перебираем трапецоиды, у которых leftp == s.p
                for tr in localizedList:
                    assert tr.leftp == s.p
                    correct = True
                    if tr.bottom != None and tr.bottom.p == s.p:
                        # TODO: предикат поворота взять из общей библиотеки
                        sign = np.sign(np.linalg.det(np.array([tr.bottom.p, tr.bottom.q]) - s.q))
                        if sign <= 0: # точка не выше
                            correct = False
                    elif tr.top != None and tr.top.p == s.p:
                        # TODO: предикат поворота взять из общей библиотеки
                        sign = np.sign(np.linalg.det(np.array([tr.top.p, tr.top.q]) - s.q))
                        if sign >= 0: # точка не ниже
                            correct = False
                    else:
                        raise Exception('Error')
                    if correct:
                        if firstTr == None:
                            # Нашли трапецоид. Он должен быть единственным
                            firstTr = tr
                        else: 
                            raise Exception('Error: нашли более 1 трапецоида')
            trNodes = firstTr.leftnb
        # Найдем, какие трапецоиды пересекает новый отрезок
        trList = intersectSegment(s, firstTr)
        lastTr = firstTr
        firstTr = next(trList, None)
        while firstTr != None:
            lastTr = next(trList, None)
            if lastTr == None: # Получили последний трапецоид
                lastTr, firstTr = firstTr, lastTr
            else: # Вставляем очередной трапецоид
                trNodes = self.__segmentInsert(s, firstTr, trNodes)
                firstTr = lastTr
        # Вставляем последний трапецоид
        self.__rightInsert(s, lastTr, trNodes)      



"Методы для отрисовки трапецоида"
def perp(a):
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def intersectionPoint(a1, a2, b1, b2):
    a1 = array([a1[0], a1[1]])
    a2 = array([a2[0], a2[1]])
    b1 = array([b1[0], b1[1]])
    b2 = array([b2[0], b2[1]])
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = dot( dap, db)
    num = dot( dap, dp )
    return (num / denom.astype(float))*db + b1

def points(trapezoid):
    q1 = [0, 0]
    q2 = [0, 5]
    q3 = [5, 5]
    q4 = [5, 0]
    if trapezoid.leftp != None:
        q1[0] = trapezoid.leftp[0]
        q2[0] = trapezoid.leftp[0]
    if trapezoid.rightp != None:
        q3[0] = trapezoid.rightp[0]
        q4[0] = trapezoid.rightp[0]
    if trapezoid.top != None:
        intp = intersectionPoint(q1, q2, trapezoid.top.p, trapezoid.top.q)
        q2[1] = intp[1]
        intp = intersectionPoint(q3, q4, trapezoid.top.p, trapezoid.top.q)
        q3[1] = intp[1]
    if trapezoid.bottom != None:
        intp = intersectionPoint(q1, q2, trapezoid.bottom.p, trapezoid.bottom.q)
        q1[1] = intp[1]
        intp = intersectionPoint(q3, q4, trapezoid.bottom.p, trapezoid.bottom.q)
        q4[1] = intp[1]
    return [q1, q2, q3, q4]

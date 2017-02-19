from TMapClasses import *

import numpy as np
from enum import Enum

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


def localize(tmap, q):
    "Возвращает список трапецоидов, в которые попала точка"
    return tmap.root.visit(q)

def updateNodeLinks(oldNode, newNode):
    "Подвешиваем новый узел в дерево вместо старого"
    for parent in oldNode.links:
        if parent.left == oldNode:
            parent.left = newNode
        elif parent.right == oldNode:
            parent.right = newNode
        else:
            raise Exception('Error')

def updateLeftNb(oldTr, newTr, indexes):
    "Обновим левых соседей у трапецоида"
    for i in indexes:
        if oldTr.leftnb[i] != None:
            # Трапецоиды могут быть соседними только по 1 ссылке, проверяем это
            if oldTr.leftnb[i].rightnb[0] == oldTr:
                j = 0
            elif oldTr.leftnb[i].rightnb[1] == oldTr:
                j = 1
            else:
                raise Exception('Error')
            oldTr.leftnb[i].rightnb[j] = newTr

def updateRightNb(oldTr, newTr, indexes):
    "Обновим правых соседей у трапецоида"
    for i in indexes:
        if oldTr.rightnb[i] != None:
            # Трапецоиды могут быть соседними только по 1 ссылке, проверяем это
            if oldTr.rightnb[i].leftnb[0] == oldTr:
                j = 0
            elif oldTr.rightnb[i].leftnb[1] == oldTr:
                j = 1
            else:
                raise Exception('Error')
            oldTr.rightnb[i].leftnb[j] = newTr

def insertSegment(tmap, s, parent):
    "Метод для вставки отрезка, попавшего целиком в трапецоид"
    # Создаем 4 новых трапецоида
    up = Trapezoid(parent.top, s, s.p, s.q)
    down = Trapezoid(s, parent.bottom, s.p, s.q)
    left = Trapezoid(parent.top, parent.bottom, parent.leftp, s.p)
    right = Trapezoid(parent.top, parent.bottom, s.q, parent.rightp)
    # Запоминаем их
    tmap.tr.append(up)
    tmap.tr.append(down)
    tmap.tr.append(left)
    tmap.tr.append(right)
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
    updateLeftNb(parent, left, [0, 1])
    updateRightNb(parent, right, [0, 1])
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
    updateNodeLinks(parent.node, pNode)
    # Удалим старый трапецоид
    tmap.tr.remove(parent)
    # Обновим корень, если это первое добавление
    if type(tmap.root) == type(upNode):
        tmap.root = pNode
    
def leftInsert(tmap, s, parent):
    "Метод для вставки отрезка в самый левый трапецоид. Отрезок пересекает как минимум 2 трапецоида!"
    # TODO: сравнить левые точки лексикографически, может и не надо создавать
    assert s.p != parent.rightp # отрезок не должен был попасть в этот трапецоид
    up = Trapezoid(parent.top, s, s.p, parent.rightp)
    down = Trapezoid(s, parent.bottom, s.p, parent.rightp) # одна из rightp ещё не известна
    left = Trapezoid(parent.top, parent.bottom, parent.leftp, s.p)
    tmap.tr.append(up)
    tmap.tr.append(down)
    tmap.tr.append(left)
    up.leftnb = [left, None]
    down.leftnb = [None, left]
    left.leftnb = parent.leftnb
    left.rightnb = [up, down]
    updateLeftNb(parent, left, [0, 1])
    # TODO: предикат поворота взять из общей библиотеки
    sign = np.sign(np.linalg.det(np.array([s.p, s.q]) - parent.rightp))
    if sign == 1:
        # точка выше отрезка, нижний трапецоид не закончен
        down.rightp = None
        up.rightnb = [parent.rightnb[0], None] # нижний не известен
        updateRightNb(parent, up, [0])
    elif sign == -1:
        # точка ниже отрезка, верхний трапецоид не закончен
        up.rightp = None
        down.rightnb = [None, parent.rightnb[1]]
        updateRightNb(parent, down, [1])
    else:
        # отрезок попал в rightp
        assert parent.rightp == s.q
        up.rightnb = [parent.rightnb[0], None]
        down.rightnb = [None, parent.rightnb[1]]
        if parent.rightnb[0] != None:
            assert parent.rightnb[0].leftnb[0] == parent
            parent.rightnb[0].leftnb[0] = up
        if parent.rightnb[1] != None:
            assert parent.rightnb[1].leftnb[1] == parent
            parent.rightnb[1].leftnb[1] = down
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
    updateNodeLinks(parent.node, pNode)
    tmap.tr.remove(parent)
    return [up, down] # будем возвращать сначала верхний, а затем нижний
    
def segmentInsert(tmap, s, parent, leftNb):
    "Вставка отрезка в очередной трапецоид, возможно последний"
    # Либо верхний, либо нижний трапецоид недоделан, либо начало отрезка совпало с точкой другого отрезка
    # Определим это по левым соседям трапецоида
    if leftNb[0] != None and leftNb[0].rightp == None:
        assert parent.leftp == leftNb[1].rightp, str(parent.leftp) + str(leftNb[1].rightp)
        # новый трапецоид - нижний; верхний недоделан
        up = leftNb[0]
        down = Trapezoid(s, parent.bottom, parent.leftp, parent.rightp)
        tmap.tr.append(down)
        leftNb[1].rightnb[0] = down
        down.leftnb = [leftNb[1], parent.leftnb[1]]
        updateLeftNb(parent, down, [1])
        upNode = up.node
        downNode = TrapezoidNode(down)
    elif leftNb[1] != None and leftNb[1].rightp == None:
        assert parent.leftp == leftNb[0].rightp, str(parent.leftp) + str(leftNb[0].rightp)
        # новый трапецоид - верхний, а нижний недоделан
        down = leftNb[1]
        up = Trapezoid(parent.top, s, parent.leftp, parent.rightp)
        tmap.tr.append(up)
        leftNb[0].rightnb[1] = up
        up.leftnb = [parent.leftnb[0], leftNb[0]]
        updateLeftNb(parent, up, [0])
        upNode = TrapezoidNode(up)
        downNode = down.node
    else:
        # s.p совпадает с leftp
        assert parent.leftp == s.p
        up = Trapezoid(parent.top, s, parent.leftp, parent.rightp)
        down = Trapezoid(s, parent.bottom, parent.leftp, parent.rightp)
        tmap.tr.append(up)
        tmap.tr.append(down)
        if parent.leftnb[0] != None:
            up.leftnb = [parent.leftnb[0], None]
            updateLeftNb(parent, up, [0])
        else:
            up.leftnb = [None, None]
        if parent.leftnb[1] != None:
            down.leftnb = [None, parent.leftnb[1]]
            updateLeftNb(parent, down, [1])
        else:
            down.leftnb = [None, None]
        upNode = TrapezoidNode(up)
        downNode = TrapezoidNode(down)
    # Надо понять, верхний или нижний трапецоид продлевать
    # TODO: предикат поворота взять из общей библиотеки
    assert (not parent.isMostRight()) # не должны здесь оказаться
    sign = np.sign(np.linalg.det(np.array([s.p, s.q]) - parent.rightp))
    if sign == 1:
        # точка выше отрезка, нижний трапецоид не закончен
        down.rightp = None
        up.rightp = parent.rightp # если в прошлый раз не закончили его
        up.rightnb = [parent.rightnb[0], None]
        updateRightNb(parent, up, [0])
    elif sign == -1:
        # точка ниже отрезка, верхний трапецоид не закончен
        up.rightp = None
        down.rightp = parent.rightp # если в прошлый раз не закончили его
        down.rightnb = [None, parent.rightnb[1]]
        updateRightNb(parent, down, [1])
    else:
        # отрезок попал в вершину, значит это последний трапецоид
        up.rightnb = [parent.rightnb[0], None]
        down.rightnb = [None, parent.rightnb[1]]
        up.rightp = parent.rightp
        down.rightp = parent.rightp
    segmentNode = YNode(s, upNode, downNode)
    upNode.links.append(segmentNode)
    downNode.links.append(segmentNode)
    updateNodeLinks(parent.node, segmentNode)
    tmap.tr.remove(parent)
    return [up, down]
    
def rightInsert(tmap, s, parent, leftNb):
    "Вставка отрезка в последний трапецоид"
    # TODO: сравнить левые точки лексикографически, может и не надо создавать
    assert s.q != parent.leftp # такой трапецоид не мог тут оказаться
    # TODO: предикат поворота взять из общей библиотеки
    sign = 1 if parent.isMostRight() else np.sign(np.linalg.det(np.array([s.p, s.q]) - parent.rightp))
    if sign == 0:
        # правый конец отрезка попал в rightp
        # значит это последний трапецоид, новые создавать не надо
        assert s.q == parent.rightp
        leftNb = segmentInsert(tmap, s, parent, leftNb)
        if parent.rightnb[0] != None:
            assert parent.rightnb[0].leftnb[0] == parent
            parent.rightnb[0].leftnb[0] = leftNb[0]
        if parent.rightnb[1] != None:
            assert parent.rightnb[1].leftnb[1] == parent
            parent.rightnb[1].leftnb[1] = leftNb[1]
        return
    if leftNb[0] != None and leftNb[0].rightp == None:
        assert parent.leftp == leftNb[1].rightp, str(parent.leftp) + str(leftNb[1].rightp)
        # новый трапецоид - нижний; верхний продолжается
        up = leftNb[0]
        up.rightp = s.q
        down = Trapezoid(s, parent.bottom, parent.leftp, s.q)
        tmap.tr.append(down)
        leftNb[1].rightnb[0] = down
        down.leftnb = [leftNb[1], parent.leftnb[1]]
        updateLeftNb(parent, down, [1])
        upNode = up.node
        downNode = TrapezoidNode(down)
    elif leftNb[1] != None and leftNb[1].rightp == None:
        assert parent.leftp == leftNb[0].rightp, str(parent.leftp) + str(leftNb[0].rightp)
        # новый трапецоид - верхний, а нижний продолжается
        down = leftNb[1]
        down.rightp = s.q
        up = Trapezoid(parent.top, s, parent.leftp, s.q)
        tmap.tr.append(up)
        leftNb[0].rightnb[1] = up
        up.leftnb = [parent.leftnb[0], leftNb[0]]
        updateLeftNb(parent, up, [0])
        upNode = TrapezoidNode(up)
        downNode = down.node
    else:
        # Отрезок целиком попал в трапецоид, его левая точка совпала с leftp, а правая с rightp нет
        assert s.p == parent.leftp
        assert s.q != parent.rightp
        for i in range(2):
            if parent.leftnb[i] != None:
                assert leftNb[i] == parent.leftnb[i]
        up = Trapezoid(parent.top, s, parent.leftp, s.q)
        down = Trapezoid(s, parent.bottom, parent.leftp, s.q)
        tmap.tr.append(up)
        tmap.tr.append(down)
        up.leftnb = [leftNb[0], None]
        down.leftnb = [None, leftNb[1]]
        if leftNb[0] != None:
            leftNb[0].rightnb[0] = up
        if leftNb[1] != None:
            leftNb[1].rightnb[1] = down
        upNode = TrapezoidNode(up)
        downNode = TrapezoidNode(down)
    right = Trapezoid(parent.top, parent.bottom, s.q, parent.rightp)
    tmap.tr.append(right)
    right.leftnb = [up, down]
    up.rightnb = [right, None]
    down.rightnb = [None, right]
    right.rightnb = parent.rightnb
    updateRightNb(parent, right, [0, 1])
    # Строим новое поддерево
    rightNode = TrapezoidNode(right)
    segmentNode = YNode(s, upNode, downNode)
    qNode = XNode(s.q, segmentNode, rightNode)
    # Обновим ссылки между узлами и трапецоидами
    upNode.links.append(segmentNode)
    downNode.links.append(segmentNode)
    rightNode.links.append(qNode)
    updateNodeLinks(parent.node, qNode)
    tmap.tr.remove(parent)
    return
    
def insert(tmap, s):
    "Вставка отрезка в трапецоидную карту"
    tmap.segments.append(s)
    # локализуем первую точку
    localizedList = localize(tmap, s.p)
    firstTr = None
    if len(localizedList) == 1:
        # Левая вершина отрезка не попала на вершину другого отерзка
        firstTr = localizedList[0]
        # TODO: лексикографическое сравнение точек взять из общей библиотеки
        if firstTr.isMostLeft() or s.p[0] > firstTr.leftp[0] or (s.p[0] == firstTr.leftp[0] and s.p[1] > firstTr.leftp[1]):
            if firstTr.isMostRight() or s.q[0] < firstTr.rightp[0] or s.q[0] == firstTr.rightp[0] and s.q[1] < firstTr.rightp[1]:
                # Простой случай: вставка отрезка целиком в один трапецоид
                insertSegment(tmap, s, firstTr)
                return
        # Вставим отрезок в самый левый трапецоид
        trNodes = leftInsert(tmap, s, firstTr)
        if s.q == firstTr.rightp: # s.q попала на другую вершину, значит уже закончили вставку
            return
    else:
        # Левая вершина отрезка попала на вершину другого отерзка
        # Надо выбрать тот трапецоид, в котором пойдет новый отрезок.
        tempList = []
        for tr in localizedList:
            if tr.leftp == s.p: # Не нужны трапецоиды, у которых rightp совпала с s.p
                tempList.append(tr)
        localizedList = tempList
        assert len(localizedList) > 0
        if len(localizedList) == 1:
            # Только у одного трапецоида левая вершина совпадает с s.p
            # Это случай на рис. 2d, причем трапецоид может быть крайним правым
            firstTr = localizedList[0]
            assert firstTr.leftnb[0] != None
            assert firstTr.leftnb[0] != None
            trNodes = firstTr.leftnb
        else:
            # Узнаем между какимим top/bottom вставляется новый отрезок
            # Перебираем трапецоиды, у которых leftp == s.p
            trNodes = None
            for tr in localizedList:
                assert tr.leftp == s.p
                correct = True
                isTrCorrect = False
                if tr.bottom != None and tr.bottom.p == s.p:
                    isTrCorrect = True
                    # TODO: предикат поворота взять из общей библиотеки
                    sign = np.sign(np.linalg.det(np.array([tr.bottom.p, tr.bottom.q]) - s.q))
                    if sign <= 0: # точка должна быть выше
                        correct = False
                if tr.top != None and tr.top.p == s.p:
                    isTrCorrect = True
                    # TODO: предикат поворота взять из общей библиотеки
                    sign = np.sign(np.linalg.det(np.array([tr.top.p, tr.top.q]) - s.q))
                    if sign >= 0: # точка должна быть ниже
                        correct = False
                if not isTrCorrect:
                    raise Exception('Error')
                if correct:
                    if firstTr == None:
                        # Нашли трапецоид. Он должен быть единственным
                        firstTr = tr
                        trNodes = firstTr.leftnb
                    else: 
                        raise Exception('Error: нашли более 1 трапецоида')
            if (trNodes == None):
                raise Exception('Error: не нашли трапецоид')
        if not firstTr.isMostRight() and (firstTr.rightp[0] < s.q[0] or (firstTr.rightp[0] == s.q[0] and firstTr.rightp[1] < s.q[1])):
            trNodes = segmentInsert(tmap, s, firstTr, trNodes)
    # Найдем, какие трапецоиды пересекает новый отрезок
    trList = intersectSegment(s, firstTr)
    lastTr = firstTr
    firstTr = next(trList, None)
    while firstTr != None:
        lastTr = next(trList, None)
        if lastTr == None: # Получили последний трапецоид
            lastTr, firstTr = firstTr, lastTr
        else: # Вставляем очередной трапецоид
            trNodes = segmentInsert(tmap, s, firstTr, trNodes)
            firstTr = lastTr
    # Вставляем последний трапецоид
    rightInsert(tmap, s, lastTr, trNodes)

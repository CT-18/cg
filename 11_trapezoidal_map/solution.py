import numpy as np
from numpy import *

"""Структура, описывающая отрезок"""
class Segment():
    "Предполагаем, что p и q упорядочены лексикографически"
    def __init__(self, p, q):
        "Левая точка"
        self.p = p
        "Правая точка"
        self.q = q

"""Структура, описывающая трапецоид"""
class Trapezoid():
    def __init__(self, top, bottom, leftp, rightp):
        "Верхний и нижний отрезки"
        self.top = top
        self.bottom = bottom
        
        "Левая и правая точки"
        self.leftp = leftp
        self.rightp = rightp
        
        "Соседи трапецоида"
        self.leftnb = [None, None]
        self.rightnb = [None, None]
        
        "Ссылки на узлы локализационной структуры"
        self.links = []

"""Структура, описывающая узел локализационной структуры"""
class Node():
        def __init__(self, nodeType, s):
            "Тип узла: -1 для точки p, 0 для отрезка s, 1 для точки q"
            self.mytype = nodeType
            "Сылка на отрезок, по которому определяется направление обхода графа"
            self.segment = s
            "Левое и правое ребро"
            "Если оно ведет на другой узел, то в первой ячейке True"
            "Если на трапецоид, то False"
            "Во второй ячейке ссылка на сам узел/трапецоид"
            self.left = [None, None]
            self.right = [None, None]

class TrapezoidalMap():
    def __init__(self):
        "Список всех трапецоидов, для отрисовки"
        self.tr = [Trapezoid(None, None, None, None)]
        "Корень поисковой структуры"
        self.root = None
    
    "Локализация точки на карте"
    def localize(self, q):
        if self.root == None:
            "Пустая карта"
            return self.tr[0]
        node = self.root
        while True:
            toLeft = True
            "Выбираем, влево или вправо идти"
            if node.mytype == 0:
                "Проверяем, q выше или ниже отрезка"
                turn = np.sign(np.linalg.det(np.array([node.segment.p, node.segment.q]) - q))
                if turn == -1:
                    "Точка ниже, идем вправо"
                    toLeft = False
                "Иначе идем влево, даже если точка на отрезке"
            elif node.mytype == -1:
                if q[0] > node.segment.p[0]:
                    toLeft = False
            else:
                if q[0] > node.segment.q[0]:
                    toLeft = False
            if toLeft:
                if not node.left[0]:
                    return node.left[1]
                node = node.left[1]
            else:
                if not node.right[0]:
                    return node.right[1]
                node = node.right[1]
        
    "Метод для вставки отрезка, попавшего целиком в трапецоид"
    def __insertInside(self, s, parent):
        "Создаем 3 новых трапецоида"
        up = Trapezoid(parent.top, s, s.p, s.q)
        down = Trapezoid(s, parent.bottom, s.p, s.q)
        right = Trapezoid(parent.top, parent.bottom, s.q, parent.rightp)
        self.tr.append(up)
        self.tr.append(down)
        self.tr.append(right)
        "Достраиваем текущий трапецоид"
        parent.rightp = s.p
        "Расставляем соседей"
        right.rightnb = parent.rightnb
        parent.rightnb = [up, down]
        up.leftnb = [parent, None]
        up.rightnb = [right, None]
        down.leftnb = [None, parent]
        down.rightnb = [None, right]
        right.leftnb = [up, down]
        "Построим новое поддерево"
        p = Node(-1, s)
        q = Node(1, s)
        seg = Node(0, s)
        p.left = [False, parent]
        p.right = [True, q]
        q.left = [True, seg]
        q.right = [False, right]
        seg.left = [False, up]
        seg.right = [False, down]
        "Обновим ссылки между узлами и трапецоидами"
        right.links.append(q)
        up.links.append(seg)
        down.links.append(seg)
        for node in parent.links:
            if node.left == [False, parent]:
                node.left = [True, p]
            elif node.right == [False, parent]:
                node.right = [True, p]
            else:
                raise Exception('Error')
        parent.links = [p]
        if self.root == None:
            self.root = p        

    "Вставка отрезка в трапецоидную карту"
    def insert(self, s):
        trapezoid = self.localize(s.p)
        "TODO: дописать вставку"
        self.__insertInside(s, trapezoid)

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
    return [[q1[0], q2[0], q3[0], q4[0], q1[0]], [q1[1], q2[1], q3[1], q4[1], q1[1]]]

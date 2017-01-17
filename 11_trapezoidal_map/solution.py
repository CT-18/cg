import numpy as np
from numpy import *

"""Структура, описывающая отрезок"""
class Segment():
    p = [0.0, 0.0]
    "Правая точка"
    q = [1.0, 1.0]
    
    "Предполагаем, что p и q упорядочены лексикографически"
    def __init__(self, p, q):
        self.p = p
        self.q = q

"""Структура, описывающая трапецоид"""
class Trapezoid():
    "Верхний и нижний отрезки"
    top = None
    bottom = None

    "Левая и правая точки"
    leftp = None
    rightp = None
    
    "Соседи трапецоида"
    leftnb = [None, None]
    rightnb = [None, None]
    
    "Ссылки на узлы локализационной структуры"
    links = [None]
    
    def __init__(self, top, bottom, leftp, rightp):
        self.top = top
        self.bottom = bottom
        self.leftp = leftp
        self.rightp = rightp
        self.links = []

class Node():
        "-1 для точки p; 0 для отрезка; 1 для точки q"
        mytype = 0
        segment = None
        left = [None, None] # нужно знать, куда ведет ребро: на узел или на трапецоид 
        right = [None, None] # False - трапецоид, True - узел
        def __init__(self, nodeType, s):
            self.mytype = nodeType
            self.segment = s

class TrapezoidalMap():
    "Список всех трапецоидов, для отрисовки"
    tr = []
    "Корень поисковой структуры"
    root = None

    def __init__(self):
        self.tr = [Trapezoid(None, None, None, None)]
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

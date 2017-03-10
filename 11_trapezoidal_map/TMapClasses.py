import numpy as np
from cg import Point , turn


class Segment:
    """Класс, описывающий отрезок"""

    def __init__(self, p: Point, q: Point):
        # Точки p и q упорядочены лексикографически"
        assert p < q
        self.p = p  # Левая точка
        self.q = q  # Правая точка


class Trapezoid:
    """Класс, описывающий трапецоид"""

    def __init__(self, top: Segment, bottom: Segment, leftp: Point, rightp: Point):
        # Верхний и нижний отрезки
        self.top = top
        self.bottom = bottom

        # Левая и правая точки
        self.leftp = leftp
        self.rightp = rightp

        # Соседи трапецоида
        self.leftnb = [None, None]
        self.rightnb = [None, None]

        # Ссылка на узел локализационной структуры
        self.node = None

    def is_rightmost(self):
        # Является ли трапецоид крайним правым
        return self.rightp is None

    def is_leftmost(self):
        # Является ли трапецоид крайним левым
        return self.leftp is None


class AbstractNode:
    """Базовый класс узла локализационной структуры"""

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def visit(self, s):
        """Возвращает трапецоид, в котором лежит точка"""
        pass


class XNode(AbstractNode):
    """Узел для точки"""

    def __init__(self, point, left, right):
        super().__init__(left, right)
        self.point = point

    def visit(self, s):
        # Порядок обхода задается лексикографическим сравнением точек
        return self.left.visit(s) if s.p < self.point else self.right.visit(s)

    __name__ = 'XNode'


class YNode(AbstractNode):
    """Узел для отрезка"""

    def __init__(self, segment, left, right):
        super().__init__(left, right)
        self.segment = segment

    def visit(self, s):
        # Порядок обхода задает предикат поворота
        sign = turn(s.p, self.segment.p, self.segment.q)
        if sign != 0:
            return self.left.visit(s) if sign == 1 else self.right.visit(s)
        else:
            # У отрезков общая левая точка, надо проверить поворот по правой точке отрезка
            assert self.segment.p == s.p
            assert not self.segment.q == s.q
            sign = turn(s.q, self.segment.p, self.segment.q)
            if sign == 0:
                raise Exception('Error')
            return self.left.visit(s) if sign == 1 else self.right.visit(s)

    __name__ = 'YNode'


class TrapezoidNode(AbstractNode):
    """Узел для трапецоида"""

    def __init__(self, trapezoid):
        super().__init__()
        # Ссылка на трапецоид
        self.tr = trapezoid
        trapezoid.node = self
        # Ссылки на все узлы, которые указывают на трапецоид
        self.links = []

    def visit(self, point):
        return self.tr

    __name__ = 'TrapezoidNode'


class TrapezoidMap():
    def __init__(self):
        # Список всех трапецоидов на карте, изначально имеется единственный "пустой" трапецоид
        self.tr = [Trapezoid(None, None, None, None)]
        # Список вставленных отрезков
        self.segments = []
        # Корень поисковой структуры
        # Изначально в него помещается узел, соответствующий "пустому" трапецоиду
        self.root = TrapezoidNode(self.tr[0])

import numpy as np

class Segment:
    "Класс, описывающий отрезок"
    
    def __init__(self, p, q):
        # Точки p и q упорядочены лексикографически"
        self.p = p # Левая точка
        self.q = q # Правая точка


class Trapezoid:
    "Класс, описывающий трапецоид"
    
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
        
        # Ссылка на узел локализационной структуры
        self.node = None
     
    def isMostRight(self):
        # Является ли трапецоид крайним правым
        return self.rightp == None
    
    def isMostLeft(self):
        # Является ли трапецоид крайним левым
        return self.leftp == None


class AbstractNode:
    "Базовый класс узла локализационной структуры"
    
    def __init__(self, left = None, right = None):
        self.left = left
        self.right = right
    
    def visit(self, q):
        # Возвращает список трапецоидов, которым принадлежит точка
        pass

class XNode(AbstractNode):
    
    def __init__(self, point, left, right):
        AbstractNode.__init__(self, left, right)
        self.point = point

    def visit(self, point):
        # Порядок обхода задается лексикографическим сравнением точек
        if point[0] < self.point[0]:
            return self.left.visit(point)
        elif point[0] > self.point[0]:
            return self.right.visit(point)
        else:
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
        # Порядок обхода задает предикат поворота
        turn = np.sign(np.linalg.det(np.array([self.segment.p, self.segment.q]) - point))
        if turn == -1:
            return self.right.visit(point)
        elif turn == 1:
            return self.left.visit(point)
        else: # turn == 0
            return self.left.visit(point) + self.right.visit(point)


class TrapezoidNode(AbstractNode):
    
    def __init__(self, trapezoid):
        AbstractNode.__init__(self)
        # Ссылка на трапецоид
        self.tr = trapezoid
        trapezoid.node = self
        # Ссылки на все узлы, которые указывают на трапецоид
        self.links = []

    def visit(self, point):
        return [self.tr]


class TrapezoidMap():
    
    def __init__(self):
        # Список всех трапецоидов на карте, изначально имеется единственный "пустой" трапецоид
        self.tr = [Trapezoid(None, None, None, None)]
        # Список вставленных отрезков
        self.segments = []
        # Корень поисковой структуры
        # Изначально в него помещается узел, соответствующий "пустому" трапецоиду
        self.root = TrapezoidNode(self.tr[0])
from fractions import *
from enum import Enum
Type = Enum('Type', 'left right inter')


class Point:
    __slots__ = ("x", "y", "det")

    def __init__(self, x=0, y=0, det=1):
        self.x = x
        self.y = y
        self.det = det

    def __add__(self, p):
        return Point(Fraction(self.x, self.det) + Fraction(p.x, p.det),
                     Fraction(self.y, self.det) + Fraction(p.y, p.det))

    def __sub__(self, p):
        return Point(Fraction(self.x, self.det) - Fraction(p.x, p.det),
                     Fraction(self.y, self.det) - Fraction(p.y, p.det))

    def __neg__(self):
        return Point(-self.x, -self.y, self.det)

    def __lt__(self, p):
        return Fraction(self.x, self.det) < Fraction(p.x, p.det) or \
               Fraction(self.x, self.det) == Fraction(p.x, p.det) and Fraction(self.y, self.det) < Fraction(p.y, p.det)

    def __eq__(self, p):
        return Fraction(self.x, self.det) == Fraction(p.x, p.det) and \
               Fraction(self.y, self.det) == Fraction(p.y, p.det)

    def __gt__(self, p):
        return not (self < p or self == p)

    def __hash__(self):
        return hash(tuple([Fraction(self.x, self.det), Fraction(self.y, self.det)]))

    def __repr__(self):
        return "(%r, %r)" % (str(Fraction(self.x, self.det)), str(Fraction(self.y, self.det)))


class Segment:
    __slots__ = ("a", "b", "id")

    def __init__(self, a, b, id):
        self.a = min(a, b)
        self.b = max(a, b)
        self.id = id

    def __lt__(self, s):
        if s is None:
            return False
        if self.id == s.id:
            return False
        if self.a == s.a:
            return self.b < s.b
        return self.a < s.a

    def __eq__(self, s):
        return self.id == s.id

    def __gt__(self, p):
        return not (self < p or self == p)

    def __repr__(self):
        return "[%r, %r]" % (self.a, self.b)


class Type(Enum):
    left = 0
    right = 1
    inter = 2

    def __lt__(self, other):
        return self.value < other.value


class Event:
    __slots__ = ("segment", "t", "addit_segment", "inter_point")        # addit_segment & inter_point are used only for type = inter

    def __init__(self, segment, t, addit_segment = None, inter_point = None):
        self.segment = segment
        self.t = t
        self.addit_segment = addit_segment
        self.inter_point = inter_point

    def __lt__(self, e):
        a = self.segment.a if self.t == Type.left else \
            self.segment.b if self.t == Type.right else self.inter_point
        b = e.segment.a if e.t == Type.left else \
            e.segment.b if e.t == Type.right else e.inter_point
        if a == b:
            if self.t == e.t:
                if self.segment == e.segment:
                    return self.addit_segment < e.addit_segment
                return self.segment < e.segment
            return self.t < e.t
        return a < b

    def __eq__(self, e):
        return self.t == e.t and \
               self.segment.id == e.segment.id and \
               (self.addit_segment is None and e.addit_segment is None or
                self.addit_segment is not None and e.addit_segment is None and self.addit_segment == e.addit_segment)

    def __gt__(self, e):
        return not (self == e or self < e)

    def __repr__(self):
        if type != Type.inter:
            return "Event [%r, type = %r]" % (self.segment, self.t)
        return "Event inter [%r, %r, point = %r]" % (self.segment, self.addit_segment, self.inter_point)
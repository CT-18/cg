import numpy as np
from decimal import *

getcontext().prec = 70

class Point:
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y

    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)

    def __repr__(self):
        return "(%r, %r)" % (self.x, self.y)

class Segment:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __lt__(self, s):
        return self.a < s.a or self.a == s.a and self.b < s.b

    def __repr__(self):
        return "[%r, %r]" % (self.a, self.b)

def calculate_det(a, b):
    return a.x * b.y - b.x * a.y

def calculate_arg(a, b):
    return abs(a.x * b.y) + abs(b.x * a.y)

def turn(s, c):
    a = s.a
    b = s.b
    e = 8 * np.finfo(float).eps * calculate_arg(b - a, c - a)
    det = calculate_det(b - a, c - a)
    if det > e:
        return 1
    if det < -e:
        return -1

    la = Point(Decimal(a.x), Decimal(a.y))
    lb = Point(Decimal(b.x), Decimal(b.y))
    lc = Point(Decimal(c.x), Decimal(c.y))
    ldet = calculate_det(lb - la, lc - la)
    if ldet > 0:
        return 1
    if ldet < 0:
        return -1
    return 0

def convert_by_x(s):    # s.a.x <= s.b.x
    if s.a.x > s.b.x:
        s.a, s.b = s.b, s.a
    return s

def convert_by_y(s):    # s.a.y <= s.b.y
    if s.a.y > s.b.y:
        s.a, s.b = s.b, s.a
    return s

def bounding_box(s1, s2):
    convert_by_x(s1)
    convert_by_x(s2)
    if not (s1.a.x <= s2.b.x and s1.b.x >= s2.a.x):
        return 0
    convert_by_y(s1)
    convert_by_y(s2)
    if not (s1.a.y <= s2.b.y and s1.b.y >= s2.a.y):
        return 0
    return 1

def check_intersection(s1, s2):
    if bounding_box(s1, s2) == 0:
        return 0
    if turn(s1, s2.a) * turn(s1, s2.b) > 0:
        return 0
    if turn(s2, s1.a) * turn(s2, s1.b) > 0:
        return 0
    return 1
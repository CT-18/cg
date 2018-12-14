import numpy as np
from entities import Point


def point_belongs_to_segment(p, a, b):  # as we know both segments lay on the same line
    left, right, p_ = 0, 0, 0
    if a.x == b.x:
        left, right, p_ = a.y, b.y, p.y
    else:
        left, right, p_ = a.x, b.x, p.x
    if left > right:
        left, right = right, left
    return left <= p_ <= right


def get_intersection_point(a, b, c, d):
    left = [[d.x - c.x, a.x - b.x],
            [d.y - c.y, a.y - b.y]]
    right = [[b.x * a.y - b.y * a.x],
             [d.x * c.y - d.y * c.x]]
    numerator = np.matmul(left, right)
    denominator = (a.y - b.y) * (d.x - c.x) - (b.x - a.x) * (c.y - d.y)
    if denominator != 0:
        return Point(numerator[0][0], numerator[1][0], denominator)
    p = None
    if point_belongs_to_segment(a, c, d):
        p = a
    elif point_belongs_to_segment(b, c, d):
        p = b
    elif point_belongs_to_segment(c, a, b):
        p = c
    elif point_belongs_to_segment(d, a, b):
        p = d
    if p is None:
        raise Exception('Incorrect test!')
    return p


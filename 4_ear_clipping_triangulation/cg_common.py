import numpy as np
#from cg import turn
from hidden import turn

def point_belongs_to_segment(p, a, b):  # as we know both segments lay on the same line
    left, right, p_ = 0, 0, 0
    if a[0] == b[0]:
        left, right, p_ = a[1], b[1], p[1]
    else:
        left, right, p_ = a[0], b[0], p[0]
    if left > right:
        left, right = right, left
    return left <= p_ <= right


def get_intersection_point(a, b, c, d):
    left = [[d[0] - c[0], a[0] - b[0]],
            [d[1] - c[1], a[1] - b[1]]]
    right = [[b[0] * a[1] - b[1] * a[0]],
             [d[0] * c[1] - d[1] * c[0]]]
    numerator = np.matmul(left, right)
    denominator = (a[1] - b[1]) * (d[0] - c[0]) - (b[0] - a[0]) * (c[1] - d[1])
    if denominator != 0:
        return np.array([numerator[0][0], numerator[1][0], denominator])
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
    return np.array([p[0], p[1], 1])

# Проверка на принадлежность точки пересечению полуплоскостей
def surf_intersection(point, *lines):
    for line in lines:
        if turn(line[0], line[1], point) < 0:
            return False
    return True

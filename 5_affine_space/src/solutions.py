import numpy as np


def orientation(points, p):
    """Возвращает ориентацию точки p относительно точек points (0, 1 или -1)."""
    return np.sign(np.linalg.det(np.array(points) - p))


def do_intersect(a, b, c, d):
    """Возвращает True, если отрезки ab и cd пересекаются."""
    abc = orientation((a, b), c)
    abd = orientation((a, b), d)
    cda = orientation((c, d), a)
    cdb = orientation((c, d), b)

    if abc != abd and cda != cdb:
        return True
    elif abc == abd == cda == cdb == 0:
        # Less or equal
        def leq(a, b):
            return a[0] < b[0] or a[0] == b[0] and a[1] <= b[1]
        
        # l <= x <= r
        def between(x, l, r):
            return leq(l, x) and leq(x, r)
        
        if leq(b, a):
            a, b = b, a
        if leq(d, c):
            c, d = d, c
            
        return (between(c, a, b) or between(d, a, b) or
                between(a, c, d) or between(b, c, d))
    else:
        return False


def area(points):
    """Возвращает площадь многоугольника,
    заданного списком вершин points в порядке обхода по часовой стрелке."""
    result = 0

    def triangle(a, b):
        return a[0] * b[1] - a[1] * b[0]

    for i in range(len(points)):
        result += triangle(points[i - 1], points[i])

    return abs(result / 2)

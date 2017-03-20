from TMapClasses import *
from cg import Point
import solution


# Набор методов для проверки корректности локализацоинной структуры и трапецоидной карты
def segment_equal(s0, s1):
    if s0 is None:
        return s1 is None
    elif s1 is None:
        return False
    else:
        return s0.p == s1.p and s0.q == s1.q


def data_equal(tr0, tr1):
    # Проверка на то, совпадают ли точки и отрезки трапецоидов
    if tr0.leftp != tr1.leftp:
        return False
    if tr0.rightp != tr1.rightp:
        return False
    if segment_equal(tr0.top, tr1.top):
        if segment_equal(tr0.bottom, tr1.bottom):
            return True
    return False


def neighbour_equal(tr0, tr1):
    if tr0 is None:
        return tr1 is None
    elif tr1 is None:
        return False
    else:
        return data_equal(tr0, tr1)


def trapezoid_equal(tr0, tr1):
    if not data_equal(tr0, tr1):
        return False
    for i in range(2):
        if not neighbour_equal(tr0.leftnb[i], tr1.leftnb[i]):
            return False
        if not neighbour_equal(tr0.rightnb[i], tr1.rightnb[i]):
            return False
    return True


def node_equal(n0, n1):
    if n0 is None:
        return n1 is None
    elif n1 is None:
        return False
    if type(n0) != type(n1):
        return False

    if n0.__name__ == TrapezoidNode.__name__:
        if len(n0.links) != len(n1.links):
            return False
        return trapezoid_equal(n0.tr, n1.tr)
    if n0.__name__ == XNode.__name__:
        if n0.point != n1.point:
            return False
    elif n0.__name__ == YNode.__name__:
        if not segment_equal(n0.segment, n1.segment):
            return False
    return node_equal(n0.left, n1.left) and node_equal(n0.right, n1.right)


def tmap_equal(map0, map1):
    """Проверка двух трапецоидных карт на идентичность"""
    return node_equal(map0.root, map1.root)


def build_tmap():
    """Построение трапецоидной карты из примера"""
    tmap = TrapezoidMap()
    f = open("tests/example.off", "r")
    f.readline()
    line = f.readline()
    n = int(line[0:2])
    m = int(line[5:7])
    point_list = []
    i = 0
    while i < n:
        pair = f.readline().split(' ')
        point_list.append([int(pair[0]), int(pair[1])])
        i += 1
    i = 0
    while i < m:
        pair = f.readline().split(' ')
        p1 = int(pair[0]) - 1
        p2 = int(pair[1]) - 1
        p = Point(point_list[p1][0], point_list[p1][1])
        q = Point(point_list[p2][0], point_list[p2][1])
        if q < p:
            p, q = q, p
        solution.insert(tmap, Segment(p, q))
        i += 1
    f.close()
    return tmap


def intersection_test(func):
    tmap = build_tmap()
    correct = True
    with open('tests/example_segments.txt') as f:
        n = int(next(f))
        for i in range(n):
            px, py, qx, qy = [int(x) for x in next(f).split()]
            s = Segment(Point(px, py), Point(qx, qy))
            first_tr = solution.localize(tmap, s)
            answer = solution.intersect_segment(s, first_tr)
            check = func(s, first_tr)
            if type(check) == type(answer):
                temp = []
                item = next(check, None)
                while item is not None:
                    temp.append(item)
                    item = next(check, None)
                check = temp
            next_tr = next(answer, None)
            pos = 0
            while next_tr is not None:
                if pos >= len(check):
                    correct = False
                    break
                tr = check[pos]
                if not data_equal(tr, next_tr):
                    correct = False
                    break
                pos += 1
                next_tr = next(answer, None)
            if pos != len(check):
                correct = False
                break
    return correct


def simple_insert_test(insert):
    for i in range(7):
        with open('tests/' + str(i)) as f:
            n = int(next(f))
            answer = TrapezoidMap()
            check = TrapezoidMap()
            segment_list = []
            for j in range(n):
                px, py, qx, qy = [int(x) for x in next(f).split()]
                s = Segment(Point(px, py), Point(qx, qy))
                segment_list.append(s)
                solution.insert(answer, s)
                insert(check, s)
            if not tmap_equal(answer, check):
                return False
            if i in [2, 6]:
                for j in range(50):
                    answer = TrapezoidMap()
                    check = TrapezoidMap()
                    for pos in np.random.permutation(n):
                        solution.insert(answer, segment_list[pos])
                        insert(check, segment_list[pos])
                    if not tmap_equal(answer, check):
                        return False
    return True


def non_crossing_insert_test(insert):
    if not simple_insert_test(insert):
        print('Простые тесты не пройдены')
        return False
    with open('tests/7') as f:
        n = int(next(f))
        segment_list = []
        for j in range(n):
            px, py, qx, qy = [int(x) for x in next(f).split()]
            segment_list.append(Segment(Point(px, py), Point(qx, qy)))
        for j in range(10):
            answer = TrapezoidMap()
            check = TrapezoidMap()
            for pos in np.random.permutation(n):
                solution.insert(answer, segment_list[pos])
                insert(check, segment_list[pos])
            if not tmap_equal(answer, check):
                return False
    return True

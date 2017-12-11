from cg import Point, turn
import itertools as itertools

triangles = [
[Point(-2, 2), Point(3, 1), Point(-2, -4)],
[Point(1, 3), Point(0, 0), Point(5, 2)],
[Point(-5, 4), Point(5, 4), Point(0, -12)],
[Point(-3, 1), Point(0, 2), Point(-3, 3)],
[Point(-4, -1), Point(-1, -1), Point(-1, -2)],
[Point(4, 5), Point(9, 5), Point(6, 2)],
[Point(4, 3), Point(6, 6), Point(9, 3)]
]

def overlap(a, b):
    if a[0] <= b[0] and b[1] <= a[1]:
        return True
    if a[0] <= b[0] and b[0] <= a[1]:
        return True
    return False


def intersect_segments(a, b):
    if turn(a[0], a[1], b[0]) * turn(a[0], a[1], b[1]) == 1:
        return False
    if turn(b[0], b[1], a[0]) * turn(b[0], b[1], a[1]) == 1:
        return False
    x1, y1 = a[0].coord[0], a[0].coord[1]
    x2, y2 = a[1].coord[0], a[1].coord[1]
    x3, y3 = b[0].coord[0], b[0].coord[1]
    x4, y4 = b[1].coord[0], b[1].coord[1]

    xx1 = [min(x1, x2), max(x1, x2)]
    xx2 = [min(x3, x4), max(x3, x4)]

    yy1 = [min(y1, y2), max(y1, y2)]
    yy2 = [min(y3, y4), max(y3, y4)]

    return (overlap(xx1, xx2) or overlap(xx2, xx1)) and (overlap(yy1, yy2) or pverlap(yy2, yy1))


def is_inside(triangle, point):
    for i in range(3):
        if turn(triangle[i], triangle[(i + 1) % 3], point) * turn(triangle[i], triangle[(i + 1) % 3], triangle[(i + 2) % 3]) < 0:
            return False

    return True


def intersect(a, b):
    for v in a:
        if is_inside(b, v):
            return True
    for v in b:
        if is_inside(a, v):
            return True

    for u, v in itertools.product(a, a):
        if u != v:
            for p, q in itertools.product(b, b):
                if p != q:
                    if intersect_segments([u, v], [p, q]):
                        return True
    return False


def test_triangles_intersection(solution):
    test_number = 1
    for a in triangles:
        for b in triangles:
            print("Test #", test_number, ": ", sep="", end="")
            if intersect(a, b) != solution(a, b):
                print("Incorrect answer\nInput data: ", end="\n")
                print("a: ", a, end="\n")
                print("b: ", b, end="\n")
                return
            print("passed", end="\n")
            test_number += 1
    print(test_number, " of ", test_number, " tests passed", sep="", end="\n")


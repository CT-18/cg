from test_utils import turn

triangles = [
[(-2, 2), (3, 1), (-2, -4)],
[(1, 3), (0, 0), (5, 2)],
[(-5, 4), (5, 4), (0, -12)],
[(-3, 1), (0, 2), (-3, 3)],
[(-4, -1), (-1, -1), (-1, -2)]
]

def is_inside(triangle, point):
    for i in range(3):
        if turn(triangle[i], triangle[(i + 1) % 3], point) * turn(triangle[i], triangle[(i + 1) % 3], triangle[(i + 2) % 3]) < 0:
            return False
    return True


def intersect(a, b):
    for v in a:
        if is_inside(a, v):
            return True
    for v in b:
        if is_inside(b, v):
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


import numpy as np
from entities import Point, Segment

import exercise_1_tests
import Bentley_Ottmann_tests


def check_first_exercise(plt, get_intersection_point):
    test = exercise_1_tests.test
    
    def calculate_det(a, b):
        return a.x * b.y - b.x * a.y

    def bounding_box(p, a, b):
        if a > b:
            a, b = b, a
        return a <= p <= b

    def check_overlap(p, a, b):
        orientation = np.sign(calculate_det(b - a, p - a))
        if orientation != 0:
            return False
        return bounding_box(p.x, a.x, b.x) and bounding_box(p.y, a.y, b.y)

    def drow_points(axis, points, color):
        for point in points:
            axis.scatter(point.x, point.y, c=color, s=40)

    def drow_segments(axis, a, b, color):
        axis.plot([a.x, b.x], [a.y, b.y], c=color)

    f, axes = plt.subplots(2, 4, figsize=(11, 6))
    print("Part 1. Intersection tests")
    for i, axis in zip(range(1, 9), axes.reshape(8)):
        axis.set_title("Test " + str(i))
        a, b, c, d, answ = test(i)
        output = get_intersection_point(a, b, c, d)
        drow_points(axis, [a, b], 'r')
        drow_segments(axis, a, b, 'r')
        drow_points(axis, [c, d], 'b')
        drow_segments(axis, c, d, 'b')
        if output == answ:
            print("Test", i, "Ok")
        else:
            print("Test", i, "Failed:")
            print("\t", answ, "expected but", output, "found")
    print("Part 2. Overlap tests")
    for i in range(9, 21):
        a, b, c, d = test(i)
        output = get_intersection_point(a, b, c, d)
        if check_overlap(output, a, b) and check_overlap(output, c, d):
            print("Test", i, "Ok")
        else:
            print("Test", i, "Fail")
            print("\ta={}, b={}, c={}, d={}".format(a, b, c, d))
            print("\tYour answer:", output)

    plt.show()


def check_Bentley_Ottmann_algorithm(plt, find_intersections):
    test = Bentley_Ottmann_tests.test

    f, axes = plt.subplots(2, 3, figsize=(10, 6))
    for i, axis in zip(range(1, 7), axes.reshape(6)):
        axis.set_title("Test " + str(i))
        input = test(i)
        n = input[0]  # number of segments
        segments = []
        for j in range(0, n):
            x1, y1, x2, y2 = map(int, input[1][j].split())
            s = Segment(Point(x1, y1), Point(x2, y2), j)
            segments.append(s)
            axis.plot([x1, x2], [y1, y2], c='black')
            axis.scatter(x1, y1, c='black', s=30)
            axis.scatter(x2, y2, c='black', s=30)
        intersection_points = find_intersections(segments)
        # TODO: add comparison

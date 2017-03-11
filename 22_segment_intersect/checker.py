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
            print("\tx={}, y={}, det={}".format(answ.x, answ.y, answ.det), "expected but\n",
                  "\tx={}, y={}, det={}".format(output.x, output.y, output.det), "found")
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

    f, axes = plt.subplots(2, 5, figsize=(12, 6))
    for i, axis in zip(range(1, 11), axes.reshape(10)):
        axis.set_title("Test " + str(i))
        input = test(i)
        n = input[0]  # number of segments
        segments = []
        for j in range(0, 2 * n, 2):
            p1, p2 = input[1][j], input[1][j + 1]
            s = Segment(p1, p2, j)
            segments.append(s)
            axis.plot([p1.x, p2.x], [p1.y, p2.y], c='black')
            axis.scatter(p1.x, p1.y, c='black', s=30)
            axis.scatter(p2.x, p2.y, c='black', s=30)
        intersection_points = find_intersections(segments)
        intersection_points_answ = set()
        intersection_points_answ.update(input[2])
        if intersection_points == intersection_points_answ:
            print("Test", i, "Ok")
        else:
            print("Test", i, "Fail:")
            print("\t", intersection_points_answ, "expected but")
            print("\t", intersection_points if len(intersection_points) > 0 else "{}", "found")

    plt.show()

from fractions import *
import numpy as np

import exercise_1_tests
import Bentley_Ottmann_tests


def check_first_exercise(plt, get_intersection_point):
    test = exercise_1_tests.test
    
    def calculate_det(a, b):
        return a[0] * b[1] - b[0] * a[1]

    def bounding_box(p, a, b):
        if a > b:
            a, b = b, a
        return a <= p <= b    

    def check_overlap(p, a, b):
        orientation = np.sign(calculate_det(b - a, p - a))
        if orientation != 0:
            return False
        return bounding_box(p[0], a[0], b[0]) and bounding_box(p[1], a[1], b[1])

    def drow_points(axis, points, color):
        for point in points:
            axis.scatter(point[0], point[1], c=color, s=40)

    def drow_segments(axis, a, b, color):
        axis.plot([a[0], b[0]], [a[1], b[1]], c=color)

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
        if Fraction(answ[0], answ[2]) == Fraction(output[0], output[2]) \
                and Fraction(answ[1], answ[2]) == Fraction(output[1], output[2]):
            print("Test", i, "Ok")
        else:
            print("Test", i, "Failed:")
            print("\t[x= {}, y= {}, det= {}]".format(answ[0], answ[1], answ[2]), "expected but")
            print("\t[x= {}, y= {}, det= {}]".format(output[0], output[1], output[2]), "found")
    print("Part 2. Overlap tests")
    for i in range(9, 21):
        a, b, c, d = test(i)
        output = get_intersection_point(a, b, c, d)
        if check_overlap(output[:2] / output[2], a, b) and check_overlap(output[:2] / output[2], c, d):
            print("Test", i, "Ok")
        else:
            print("Test", i, "Fail")
            print("\ta={}, b={}, c={}, d={}".format(a, b, c, d))
            print("\tYour answer:", output)

    plt.show()

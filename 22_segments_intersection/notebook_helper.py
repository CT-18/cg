import matplotlib.pyplot as plt
import numpy as np
import bentley_ottman_helper
import test_utils
import plotlib_utils
import geometry_utils


def intro():
    plotlib_utils.draw(plt)


def show_configuration(plt, segments, intersections_student):
    plt.xlabel('x-coordinate')
    plt.ylabel('y-coordinate')
    plt.xlim([-10, 10])
    plt.ylim([-10, 10])
    plotlib_utils.draw_segment(plt, segments)
    plotlib_utils.draw_points(plt, intersections_student)
    plt.show()


def silly_algorithm_testing(algorithm, logging=True):
    tests = 1000
    for i in range(tests):
        n = 10
        segments = test_utils.generate_segments(8, n)
        intersections_correct = bentley_ottman_helper.segments_intersection_n2(segments)
        intersections_student = algorithm(segments)
        if sorted(intersections_student) != sorted(intersections_correct):
            
            print("Some intersections not found\n")
            print("correct: ", intersections_correct)
            print("output: ", intersections_student)
            show_configuration(plt, segments, intersections_student)
            return
        if logging and (i + 1) % 100 == 0:
            print(i + 1, " tests done")

        if i == tests - 1:
            print("Correct solution")
            show_configuration(plt, segments, intersections_student)


def segments_intersection_set_testing(segments_intersection_set):
    c = 10
    tests = 1000
    for i in range(tests):
        [f, s] = test_utils.generate_segments_on_line(c, 2)

        intersection_set = segments_intersection_set(f, s)
        intersection_set_correct = bentley_ottman_helper.segments_intersection_set(f, s)
        if not np.array_equal(intersection_set, intersection_set_correct):
            print("Incorrect")
            print(f)
            print(s)
            print("correct=", intersection_set_correct)
            print("output=", intersection_set)
        if (i + 1) % 100 == 0:
            print(i + 1, " tests done")
    print("Correct solution")


def show_turn_predicate():
    plotlib_utils.draw_figure(plt, geometry_utils.orientation_exact, 5, 0.5)


def intersection_checking_testing(do_intersect):
    c = 10
    tests = 1000
    for i in range(tests):
        [f, s] = test_utils.generate_segments(c, 2)

        b1 = do_intersect(f, s)
        b2 = bentley_ottman_helper.do_intersect(f, s)
        if b1 != b2:
            print("Incorrect")
            print("correct=", b2)
            print("output=", b1)
            plotlib_utils.draw_segment(plt, [f, s])
            plt.show()
            return
        if (i + 1) % 100 == 0:
            print(i + 1, " tests done")
    print("Correct solution")


def show_events_handle_order(logging = True):
    plt.xlabel('x-coordinate')
    plt.ylabel('y-coordinate')
    plt.title('Events type demonstration')

    segments = test_utils.generate_segments(10, 10)
    intersection = bentley_ottman_helper.segments_intersection_n2(segments)
    plotlib_utils.draw_segment(plt, segments)
    plotlib_utils.draw_points(plt, [[segment[0][0], segment[0][1]] for segment in segments], col="co")
    plotlib_utils.draw_points(plt, [[segment[1][0], segment[1][1]] for segment in segments], col="ro")
    plotlib_utils.draw_points(plt, intersection, col="go")

    # plt.ion()
    plt.show()

    all_point = sorted([[segment[0][0], segment[0][1]] for segment in segments] + [[segment[1][0], segment[1][1]] for segment in segments] + intersection)
    print("Iteration order")
    n = len(all_point)
    changed = False
    if not logging and n > 5:
        n = 5
        changed = True
    for point in all_point[:n]:
        print("{%.2f"%(point[0]) + ",", "%.2f}"%(point[1])),
    if changed:
        print("...")

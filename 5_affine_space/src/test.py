import numpy as np
from numpy import sqrt
import os


def orientation_demo(plt, orientation):
    tests = np.array([[[0, 0], [0, 2], [0, 4]],
                      [[0, 0], [-1, 2], [0, 4]],
                      [[0, 0], [1, 2], [0, 4]]])

    f, axes = plt.subplots(1, 3, figsize=(9, 3))

    for (a, p, b), axis in zip(tests, axes.reshape((3))):
        points = [a, b]
        point_array = np.array([a, p, b])
        
        axis.scatter(point_array[:,0], point_array[:,1], c='r', s=50, zorder=10)
        axis.plot(point_array[:,0], point_array[:,1], c='g')
        
        dx = np.array([0.3, 0])
        for i, q in zip([0, 1], points):
            axis.annotate('points[{}]'.format(i), xy=q, xytext=q + dx)
        axis.annotate('p', xy=p, xytext=p + dx)

        axis.set_title("sign = {}".format(orientation(points, p)))
        axis.axis([-3, 3, -1, 5])

    plt.show()


def check_polygon(plt, orientation, points, expected):
    f, axes = plt.subplots(3, 3, figsize=(10, 10))

    points_t = points.T
    points_cycled = np.concatenate((points_t, points[0][np.newaxis].T), axis=1)
    
    actual = True

    for axis, i in zip(axes.reshape((9)),
                       range(9)):
        center = points[i - 1]
        e1 = points[i] - center
        e2 = points[i - 2] - center

        turn = orientation([points[i], points[i - 2]], center)
        actual &= (turn == 1)

        axis.scatter(points_t[0,], points_t[1,], c='r', zorder=10)
        axis.plot(points_cycled[0,], points_cycled[1,], c='g')
        centers = np.array([center, center]).T
        directions = np.array([e1, e2]).T
        axis.quiver(centers[0], centers[1], directions[0], directions[1],
                    angles='xy', scale_units='xy', scale=1, width=0.02, zorder=5)
        axis.set_title("i = {}, sign = {}".format(i - 1, turn))

    print("expected = {}, actual = {}".format(expected, actual))
    print("correct" if expected == actual else "wrong answer")
    plt.show()


def test_on_args(solution, author, args):
    expected = author(*args)
    actual = solution(*args)
    if expected != actual:
        print("wrong answer")
        print("expected = {}, actual = {}".format(expected, actual))
        print("args = {}".format(args))
        return False
    return True


def orientation_test(solution, author):
    np.random.seed(239)

    def gen(dim):
        points = np.round(np.random.uniform(-10, 10, dim * dim).reshape((dim, dim)))
        p = np.round(np.random.uniform(-10, 10, dim))
        return (points, p)

    for dim in range(3, 10, 3):
        for test_i in range(10):
            args = gen(dim)
            if not test_on_args(solution, author, args):
                return

    print("correct")


def intersection_demo(plt, do_intersect):
    tests = [[[0, 0], [2, 2], [2, 0], [0, 2]],
             [[0, 0], [2, 2], [2, 0], [1, 1]],
             [[0, 0], [1, 1], [2, 0], [1, 1]],
             [[0, 0], [1, 2], [2, 0], [1, 1]],
             [[0, 0], [2, 2], [1, 1], [3, 3]],
             [[0, 0], [1, 1], [2, 2], [3, 3]]]

    f, axes = plt.subplots(2, 3, figsize=(9, 6))

    for (a, b, c, d), axis in zip(tests, axes.reshape((6))):
        ab = np.array([a, b]).T
        cd = np.array([c, d]).T
        for segment, color in [(ab, 'r'), (cd, 'g')]:
            axis.scatter(segment[0,], segment[1,], c=color, s=50, zorder=10)
            axis.plot(segment[0,], segment[1,], c=color)
        axis.set_title("Intersect" if do_intersect(a, b, c, d) else "Don't intersect")

    plt.show()


def intersection_test(solution, author):
    np.random.seed(239)

    for test_i in range(30):
        args = np.round(np.random.uniform(-10, 10, 8).reshape((4, 2)))
        if not test_on_args(solution, author, args):
            return

    print("correct")


def batman(plt, f):
    xs = np.arange(-7.25, 7.25, 0.01)
    ys = np.arange(-5, 5, 0.01)
    x, y = np.meshgrid(xs, ys)

    old_settings = np.seterr(all='ignore')

    n112 = f(4, 4) * 21 / 2
    n05 = f(1, 5) * 60
    n8 = f(4, 2)
    n33 = f(6, 3) - f(3, 1)

    eq1 = ((x/7)**2*sqrt(abs(abs(x)-3)/(abs(x)-3))+(y/3)**2*sqrt(abs(y+3/7*sqrt(n33))/(y+3/7*sqrt(n33)))-1)
    eq2 = (abs(x/2)-((3*sqrt(n33)-7)/n112)*x**2-3+sqrt(1-(abs(abs(x)-2)-1)**2)-y)
    eq3 = (9*sqrt(abs((abs(x)-1)*(abs(x)-.75))/((1-abs(x))*(abs(x)-.75)))-n8*abs(x)-y)
    eq4 = (3*abs(x)+.75*sqrt(abs((abs(x)-.75)*(abs(x)-n05))/((.75-abs(x))*(abs(x)-n05)))-y)
    eq5 = (2.25*sqrt(abs((x-n05)*(x+n05))/((n05-x)*(n05+x)))-y)
    eq6 = (6*sqrt(10)/7+(1.5-n05*abs(x))*sqrt(abs(abs(x)-1)/(abs(x)-1))-(6*sqrt(10)/14)*sqrt(4-(abs(x)-1)**2)-y)

    np.seterr(**old_settings)

    for f in [eq1,eq2,eq3,eq4,eq5,eq6]:
        plt.contour(x, y, f, [0])

    for f in [eq1,eq2,eq3,eq4,eq5,eq6]:
        plt.contour(-x, y, f, [0])

    plt.show()


def area_test(solution, author):
    test_dir = "area_test"

    test_files = os.listdir(test_dir)

    for test_file in test_files:
        file_path = os.path.join(test_dir, test_file)
        f = open(file_path)

        test = list(map(lambda line: tuple(map(lambda x: int(x),
                                               line.split(' '))),
                        f.readlines()))

        expected = author(test)
        actual = solution(test)
        if expected != actual:
            print("wrong answer")
            print("expected = {}, actual = {}".format(expected, actual))
            print("test file = {}".format(file_path))
            return

    print("correct")

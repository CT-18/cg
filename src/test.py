import numpy as np
from numpy import sqrt


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
            #points, p = gen(dim)
            #expected = author(points, p)
            #actual = solution(points, p)
            #if expected != actual:
            #    print("wrong answer")
            #    print("points = {}, p = {}".format(points, p))
            #    print("expected = {}, actual = {}".format(expected, actual))
            #    return

    print("correct")


def intersection_test(solution, author):
    np.random.seed(239)

    for test_i in range(30):
        args = np.round(np.random.uniform(-10, 10, 8).reshape((4, 2)))
        if not test_on_args(solution, author, args):
            return
        #a, b, c, d = np.round(np.random.uniform(-10, 10, 8).reshape((4, 2)))
        #expected = author(a, b, c, d)
        #actual = solution(a, b, c, d)
        #if expected != actual:
        #    print("wrong answer")
        #    print("a = {}, b = {}, c = {}, d = {}".format(a, b, c, d))
        #    print("expected = {}, actual = {}".format(expected, actual))
        #    return

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

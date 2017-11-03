import numpy as np
from sympy import convex_hull
from sympy import Line
from sympy import Point as P
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import matplotlib.pyplot as plt
from IPython.display import display


def turn(points, p):
    return np.sign(np.linalg.det(np.array(points) - p))


def generate_test(n):
    rand_points = np.random.randint(0, 25, size=(n, 2))
    points = []
    if n <= 3:
        return rand_points.tolist()
    hull = convex_hull(*rand_points)
    for point in hull.vertices:
        # points.insert(len(points), [point.x, point.y])
        points.append([point.x, point.y])
    return points


def check(points, point):
    polygon = Polygon(points)
    point = Point(point)
    return polygon.contains(Point(point))


def check_triangle(points, point):
    return check([points[0], points[1], points[2]], point)


def draw(points, point, title=""):
    fig = plt.figure(figsize=(6, 6))
    ax1 = plt.subplot(111, aspect='equal')
    ax1.plot(point[0], point[1], 'o', color='g')
    points.insert(len(points), [points[0][0], points[0][1]])
    points_t = np.array(points).T
    ax1.plot(points_t[0,], points_t[1,], '--', c='r')
    ax1.scatter(points_t[0,], points_t[1,], c='r')
    ax1.plot(points[0][0], points[0][1], '.', color='b')
    ax1.set_xlim(0 - 1, 25 + 1)
    ax1.set_ylim(0 - 1, 25 + 1)
    if title != "":
        ax1.set_title(title)
    display(fig)
    plt.close()


def test(f, col=30, n=200):
    for i in range(0, n):
        points = []
        while True:
            points = generate_test(col)
            if points[0] is points[1] or points[0][0] is points[0][1] or points[1][0] is points[1][1]:
                continue
            l = Line(P(points[0][0], points[0][1]), P(points[1][0], points[1][1]))
            if len(l.intersection(P(points[2][0], points[2][1]))) != 0:
                continue
            break

        if i % 50 == 0 and i != 0:
            print('passed {} tests'.format(i))
        for j in range(0, 2 * len(points)):
            point = np.random.randint(0, 25, size=(2))
            answer = check(points, point)
            for k in range(0, len(points) - 1):
                points.insert(len(points), points[0])
                points.remove(points[0])
                result = f(points, point)
                if result is answer:
                    continue
                print("Test №{} failed".format(i + 1))
                print("Expected {}, result {}".format(answer, result))
                print("points={}".format(points))
                print("point={}".format(point))
                draw(points, point)
                return
    print("All tests passed")


def test_triangle(f, n=200):
    test(f, 3, n)


def show_test(test, f):
    res = f(test[0], test[1])
    draw(test[0], test[1], "inside" if res else "outside")


def main():
    print()


if __name__ == '__main__':
    main()
